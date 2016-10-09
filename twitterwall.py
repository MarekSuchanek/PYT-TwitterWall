import configparser
import time
import base64
from datetime import datetime
import requests
import click
import signal
import sys

# TODO: create CLI class for printing
cli_dformat = '%d/%m/%Y %H:%M:%S'
no_style = False
colors = {
    'author': 'blue',
    'bye': 'red',
    'date': 'green',
    'hashtag': 'magenta',
    'mention': 'yellow'
}


class TwitterConnection:
    tweet_api_url = 'https://api.twitter.com/1.1/search/tweets.json'
    timeout = 5

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = self.start_session()

    def start_session(self):
        session = requests.Session()
        secret = '{}:{}'.format(self.api_key, self.api_secret)
        secret64 = base64.b64encode(secret.encode('ascii')).decode('ascii')

        headers = {
            'Authorization': 'Basic {}'.format(secret64),
            'Host': 'api.twitter.com',
        }

        r = session.post('https://api.twitter.com/oauth2/token',
                         headers=headers,
                         data={'grant_type': 'client_credentials'},
                         timeout=self.timeout)
        r.raise_for_status()

        bearer_token = r.json()['access_token']

        def bearer_auth(req):
            req.headers['Authorization'] = 'Bearer ' + bearer_token
            return req

        session.auth = bearer_auth
        return session

    def get_tweets(self, params):
        r = self.session.get(self.tweet_api_url,
                             params=params,
                             timeout=self.timeout)
        r.raise_for_status()
        return [Tweet(t) for t in reversed(r.json()['statuses'])]


class Tweet:
    """Twitter tweet data wrapper concentrating getters"""
    twitter_dformat = '%a %b %d %H:%M:%S +0000 %Y'

    def __init__(self, jsondata):
        self.data = jsondata

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    def get_id(self):
        return self.data['id']

    def get_text(self):
        return self.data['text']

    def get_author_name(self):
        return self.data['user']['name']

    def get_author_nick(self):
        return self.data['user']['screen_name']

    def get_created(self):
        return datetime.strptime(self.data['created_at'],
                                 self.twitter_dformat)

    def get_url(self):
        return 'https://twitter.com/{}/statuses/{}'.\
            format(self.get_author_nick(), self.get_id())


def click_secho(text, bold=False, fg=None, bg=None, nl=True):
    if no_style:
        click.echo(text, nl=nl)
    else:
        click.secho(text, bold=bold, fg=fg, bg=bg, nl=nl)


def tweet_highlighter(tweet_text):
    if no_style:
        return tweet_text
    words = tweet_text.split(' ')
    for i, w in enumerate(words):
        if w.startswith('#'):
            words[i] = click.style(w, fg=colors['hashtag'], bold=True)
        elif w.startswith('@'):
            words[i] = click.style(w, fg=colors['mention'], bold=True)
        elif w.startswith('http://') or w.startswith('https://'):
            words[i] = click.style(w, underline=True)
    return ' '.join(words)


def print_tweet(tweet):
    click_secho('{}'.format(tweet.get_created().strftime(cli_dformat)),
                fg=colors['date'], nl=False)
    click_secho(' ({})'.format(tweet.get_url()), fg='magenta')
    click_secho(tweet.get_author_name(), bold=True, fg=colors['author'],
                nl=False)
    click_secho(' ({})'.format(tweet.get_author_nick()),
                fg=colors['author'], nl=False)
    click.echo(': {}'.format(tweet_highlighter(tweet.get_text())))
    click.echo()


def tweets_process(twitter, params, tfilter):
    last_id = params['since_id']
    for t in twitter.get_tweets(params):
        if t.get_id() > last_id:
            last_id = t.get_id()
        if tweet_filter(t, tfilter):
            print_tweet(t)
    return last_id


def tweet_filter(tweet, tfilter):
    for rule in tfilter:
        if not tfilter[rule](tweet):
            return False
    return True


def build_filter(no_rt, rt_min, rt_max, f_min, f_max, authors, bauthors):
    tf = {}
    if no_rt:
        tf['rt'] = lambda t: 'retweeted_status' not in t

    if rt_max is not None:
        tf['rt_count'] = lambda t: rt_min < t['retweet_count'] < rt_max
    elif rt_min > 0:
        tf['rt_count'] = lambda t: rt_min < t['retweet_count']

    if f_max is not None:
        tf['user_f'] = lambda t: f_min < t['user']['followers_count'] < f_max
    elif f_min > 0:
        tf['user_f'] = lambda t: f_min < t['user']['followers_count']

    if len(authors) > 0:
        tf['user_a'] = lambda t: t['user']['screen_name'] in authors

    if len(bauthors) > 0:
        tf['user_a'] = lambda t: not t['user']['screen_name'] in bauthors

    return tf


@click.command()
@click.option('--config', '-c', default='config/auth.cfg',
              help='App config file path.')
@click.option('--query', '-q', prompt='Query',
              help='Expression to filter tweets.')
@click.option('--count', '-n', default=5,
              help='Number of initial tweets.')
@click.option('--interval', '-i', default=10,
              help='Seconds to check new tweets.')
@click.option('--lang', '-l', default=None, type=click.STRING,
              help='Language (ISO 639-1) code.')
@click.option('--author', '-a', multiple=True, type=click.STRING,
              help='Nickname of tweet author (multiple).')
@click.option('--blocked-author', '-b', multiple=True, type=click.STRING,
              help='Nickname of blocked tweet author (multiple).')
@click.option('--no-retweets', is_flag=True,
              help='Don\'t print retweets.')
@click.option('--retweets-min', default=0,
              help='Min number of retweets.')
@click.option('--retweets-max', default=None, type=click.INT,
              help='Max number of retweets.')
@click.option('--followers-min', default=0,
              help='Min number of followers.')
@click.option('--followers-max', default=None, type=click.INT,
              help='Max number of followers.')
@click.option('--no-swag', is_flag=True,
              help='Don\'t style with colors and bold font on output.')
def twitter_wall(config, query, count, interval, lang, no_retweets,
                 retweets_min, retweets_max, followers_min, followers_max,
                 author, blocked_author, no_swag):
    """Simple Twitter Wall for loading desired tweets in CLI"""
    global no_style
    no_style = no_swag

    click.clear()
    print('', end='', flush=True)

    authcfg = configparser.ConfigParser()
    authcfg.read(config)
    twitter = TwitterConnection(authcfg['twitter']['key'],
                                authcfg['twitter']['secret'])

    params = {'q': query, 'count': count, 'since_id': 0}
    if lang is not None:
        params['lang'] = lang

    tf = build_filter(no_retweets, retweets_min, retweets_max, followers_min,
                      followers_max, set(author), set(blocked_author))

    params['since_id'] = tweets_process(twitter, params, tf)
    del params['count']
    while True:
        time.sleep(interval)
        params['since_id'] = tweets_process(twitter, params, tf)


def signal_handler(sig, frame):
    click.echo()
    click_secho('Bye! See you soon...', fg=colors['bye'], bold=True)
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    twitter_wall()
