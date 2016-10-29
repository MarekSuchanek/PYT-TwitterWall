import configparser
import click
import signal
import sys
import time
from .common import TwitterConnection


class TweetReader:

    def __init__(self, twitter, wall, query, lang):
        self.twitter = twitter
        self.wall = wall
        self.params = {'q': query, 'since_id': 0}
        self.tf = {}
        if lang is not None:
            self.params['lang'] = lang

    def setup_filter(self, no_rt, rt_min, rt_max, f_min,
                     f_max, authors, bauthors):
        authors = {a.lower() for a in authors}
        bauthors = {ba.lower() for ba in bauthors}
        self.tf = {}
        if no_rt:
            self.tf['rt'] = lambda t: not t.is_retweet()

        if rt_max is not None:
            self.tf['rt_count'] = lambda t: rt_min < t.get_nretweets() < rt_max
        elif rt_min > 0:
            self.tf['rt_count'] = lambda t: rt_min < t.get_nretweets()

        if f_max is not None:
            self.tf['user_f'] = lambda t: f_min < t.get_nfollows() < f_max
        elif f_min > 0:
            self.tf['user_f'] = lambda t: f_min < t.get_nfollows()

        if len(authors) > 0:
            self.tf['user_a'] = \
                lambda t: t.get_author_nick().lower() in authors

        if len(bauthors) > 0:
            self.tf['user_b'] = \
                lambda t: t.get_author_nick().lower() not in bauthors

        return self.tf

    def process_n(self, n):
        self.params['count'] = n
        self.process_periodic()
        del self.params['count']

    def process_periodic(self):
        for t in self.twitter.get_tweets(self.params):
            if t.get_id() > self.params['since_id']:
                self.params['since_id'] = t.get_id()
            if self.tweet_filter(t):
                self.wall.print_tweet(t)

    def tweet_filter(self, tweet):
        for rule in self.tf:
            if not self.tf[rule](tweet):
                return False
        return True

    def run(self, init_cnt, interval):
        self.process_n(init_cnt)
        while True:
            time.sleep(interval)
            self.process_periodic()


class CLIWall:
    dformat = '%d/%m/%Y %H:%M:%S'

    def __init__(self):
        click.clear()
        print('', end='', flush=True)

    def print_tweet(self, tweet):
        click.echo('{}'.format(tweet.get_created().strftime(self.dformat)),
                   nl=False)
        click.echo(' ({})'.format(tweet.get_url()))
        click.echo(tweet.get_author_name(), nl=False)
        click.echo(' [{}]'.format(tweet.get_author_nick()), nl=False)
        click.echo(': {}'.format(tweet.get_text()))
        click.echo()


class CLIColorfulWall(CLIWall):
    colors = {
        'author': 'blue',
        'bye': 'red',
        'date': 'green',
        'hashtag': 'magenta',
        'mention': 'yellow'
    }

    def __init__(self):
        super().__init__()

    def print_tweet(self, tweet):
        click.secho('{}'.format(tweet.get_created().strftime(self.dformat)),
                    fg=self.colors['date'], nl=False)
        click.secho(' ({})'.format(tweet.get_url()), fg='magenta')
        click.secho(tweet.get_author_name(), bold=True,
                    fg=self.colors['author'], nl=False)
        click.secho(' [{}]'.format(tweet.get_author_nick()),
                    fg=self.colors['author'], nl=False)
        click.echo(': {}'.format(self.tweet_highlighter(tweet)))
        click.echo()

    def tweet_highlighter(self, tweet):
        text = tweet.get_text()
        result = ""
        entities = []
        for hashtag in tweet.get_entities_of_type('hashtags'):
            entities.append(
                (hashtag['indices'][0], hashtag['indices'][1],
                 click.style('#'+hashtag['text'],
                             fg=self.colors['hashtag'], bold=True))
            )
        for mention in tweet.get_entities_of_type('user_mentions'):
            entities.append(
                (mention['indices'][0], mention['indices'][1],
                 click.style('@'+mention['screen_name'],
                             fg=self.colors['mention'], bold=True))
            )
        for url in tweet.get_entities_of_type('urls'):
            entities.append(
                (url['indices'][0], url['indices'][1],
                 click.style(url['url'], underline=True))
            )
        entities.sort(reverse=True)
        index = 0
        while len(entities) > 0:
            act = entities.pop()
            result += text[index:act[0]] + act[2]
            index = act[1]
        result += text[index:]
        return result


@click.group(name="twitterwall")
@click.option('--config', '-c', default='config/auth.cfg',
              type=click.File('r'), help='App config file path.')
@click.version_option(version='0.4', prog_name='TwitterWall')
@click.pass_context
def twitter_wall(ctx, config):
    """Twitter Wall for loading and printing desired tweets"""
    authcfg = configparser.ConfigParser()
    authcfg.read_file(config)
    config.close()
    ctx.obj['API_KEY'] = authcfg['twitter']['key']
    ctx.obj['API_SECRET'] = authcfg['twitter']['secret']


@twitter_wall.command()
@click.option('--query', '-q', prompt='Query',
              help='Expression to filter tweets.')
@click.option('--count', '-n', default=5,
              help='Number of initial tweets.')
@click.option('--interval', '-i', default=10,
              help='Seconds to check new tweets.')
@click.option('--lang', '-l', default=None, type=click.STRING,
              help='Language (ISO 639-1) code.')
@click.option('--author', '-a', multiple=True, type=click.STRING,
              help='Nickname of allowed tweet author (multiple).')
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
@click.option('--swag/--no-swag', is_flag=True, default=True,
              help='Style (or not) with colors and bold/underline on output.')
@click.pass_context
def cli(ctx, query, count, interval, lang, no_retweets,
        retweets_min, retweets_max, followers_min, followers_max,
        author, blocked_author, swag):
    """Twitter Wall running in CLI"""
    twitter = TwitterConnection(ctx.obj['API_KEY'], ctx.obj['API_SECRET'])
    wall = CLIColorfulWall() if swag else CLIWall()
    signal.signal(signal.SIGINT, signal_handler)

    tr = TweetReader(twitter, wall, query, lang)
    tr.setup_filter(no_retweets, retweets_min, retweets_max, followers_min,
                    followers_max, set(author), set(blocked_author))
    tr.run(count, interval)


@twitter_wall.command()
@click.option('--debug/--no-debug', is_flag=True, default=False)
@click.option('--count', '-n', default=5,
              help='Number of tweets displayed without AJAX.')
@click.option('--interval', '-i', default=5,
              help='Interval of loading by AJAX (min 3s).')
@click.pass_context
def web(ctx, debug, count, interval):
    """Twitter Wall running as web server"""
    from .web import app
    app.config['API_KEY'] = ctx.obj['API_KEY']
    app.config['API_SECRET'] = ctx.obj['API_SECRET']
    app.config['AJAX_INTERVAL'] = interval
    app.config['INIT_COUNT'] = count
    app.config['TEMPLATES_AUTO_RELOAD'] = debug
    app.run(debug=debug)


def signal_handler(sig, frame):
    print('\nBye! See you soon...')
    sys.exit(0)
