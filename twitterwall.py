import configparser
import time
import base64
import requests
import click
import signal
import sys

tweet_api_url = 'https://api.twitter.com/1.1/search/tweets.json'


# TODO: raise_for_status request fail (or other)
def twitter_session(conf_file):
    config = configparser.ConfigParser()
    config.read(conf_file)
    api_key = config['twitter']['key']
    api_secret = config['twitter']['secret']

    session = requests.Session()
    secret = '{}:{}'.format(api_key, api_secret)
    secret64 = base64.b64encode(secret.encode('ascii')).decode('ascii')

    headers = {
        'Authorization': 'Basic {}'.format(secret64),
        'Host': 'api.twitter.com',
    }

    r = session.post('https://api.twitter.com/oauth2/token',
                     headers=headers,
                     data={'grant_type': 'client_credentials'})

    bearer_token = r.json()['access_token']

    def bearer_auth(req):
        req.headers['Authorization'] = 'Bearer ' + bearer_token
        return req

    session.auth = bearer_auth
    return session


# TODO: options + highlight hashtags & mentions
def print_tweet(tweet):
    click.echo('## {}'.format(tweet['created_at']))
    click.secho(tweet['user']['name'], bold=True, fg='blue', nl=False)
    click.secho(' ({})'.format(tweet['user']['screen_name']),
                fg='blue', nl=False)
    click.echo(': '+tweet['text'])
    click.echo()


def get_tweets(session, params):
    r = session.get(tweet_api_url, params=params)
    return reversed(r.json()['statuses'])


def tweets_process(session, params, tfilter):
    last_id = 0
    for t in get_tweets(session, params):
        if t['id'] > last_id:
            last_id = t['id']
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


# TODO: optional colors and printing options
@click.command()
@click.option('--config', '-c', default='auth.cfg',
              help='App config file path.')
@click.option('--query', '-q', prompt='Query',
              help='Expression to filter tweets.')
@click.option('--count', '-n', default=5,
              help='Number of initial tweets.')
@click.option('--interval', '-i', default=20,
              help='Seconds to check new tweets.')
@click.option('--lang', '-l', default=None, type=click.STRING,
              help='Language (ISO 639-1) code.')
@click.option('--author', '-a', multiple=True, type=click.STRING,
              help='Nickname of tweet author (multiple).')
@click.option('--blocked-author', '-b', multiple=True, type=click.STRING,
              help='Nickname of blocked tweet author (multiple).')
@click.option('--no-retweet', is_flag=True,
              help='Don\'t print retweets.')
@click.option('--retweets-min', default=0,
              help='Min number of retweets.')
@click.option('--retweets-max', default=None, type=click.INT,
              help='Max number of retweets.')
@click.option('--followers-min', default=0,
              help='Min number of followers.')
@click.option('--followers-max', default=None, type=click.INT,
              help='Max number of followers.')
def twitter_wall(config, query, count, interval, lang, no_retweet, retweets_min,
                 retweets_max, followers_min, followers_max, author,
                 blocked_author):
    """Simple Twitter Wall for loading desired tweets in CLI"""
    session = twitter_session(config)
    params = {'q': query, 'count': count}
    if lang is not None:
        params['lang'] = lang

    click.clear()
    tf = build_filter(no_retweet, retweets_min, retweets_max, followers_min,
                      followers_max, set(author), set(blocked_author))

    params['since_id'] = tweets_process(session, params, tf)
    del params['count']
    while True:
        time.sleep(interval)
        params['since_id'] = tweets_process(session, params, tf)


def signal_handler(sig, frame):
    click.echo()
    click.secho('Bye! See you soon...', fg='red', bold=True)
    sys.exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    twitter_wall()
