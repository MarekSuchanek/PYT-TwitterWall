import configparser
import click
import signal
import sys
from common import *
from web import app

wall = None
twitter = None


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

    def print_bye(self, text):
        click.echo()
        click.echo(text)


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
        click.echo(': {}'.format(self.tweet_highlighter(tweet.get_text())))
        click.echo()

    def tweet_highlighter(self, tweet_text):
        words = tweet_text.split(' ')
        for i, w in enumerate(words):
            if Tweet.is_hashtag(w):
                words[i] = click.style(w, fg=self.colors['hashtag'], bold=True)
            elif Tweet.is_mention(w):
                words[i] = click.style(w, fg=self.colors['mention'], bold=True)
            elif Tweet.is_hyperref(w):
                words[i] = click.style(w, underline=True)
        return ' '.join(words)

    def print_bye(self, text):
        click.echo()
        click.secho(text, fg=self.colors['bye'], bold=True)


@click.group()
@click.option('--config', '-c', default='config/auth.cfg',
              type=click.File('r'), help='App config file path.')
def twitter_wall(config):
    """Twitter Wall for loading and printing desired tweets"""
    global twitter
    authcfg = configparser.ConfigParser()
    authcfg.read_file(config)
    config.close()
    twitter = TwitterConnection(authcfg['twitter']['key'],
                                authcfg['twitter']['secret'])


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
@click.version_option(version='0.1.1', prog_name='TwitterWall CLI')
def cli(query, count, interval, lang, no_retweets,
        retweets_min, retweets_max, followers_min, followers_max,
                 author, blocked_author, swag):
    """Twitter Wall running in CLI"""
    global wall, twitter
    wall = CLIColorfulWall() if swag else CLIWall()
    signal.signal(signal.SIGINT, signal_handler)

    tr = TweetReader(twitter, wall, query, lang)
    tr.setup_filter(no_retweets, retweets_min, retweets_max, followers_min,
                    followers_max, set(author), set(blocked_author))
    tr.run(count, interval)


@twitter_wall.command()
@click.option('--debug/--no-debug', is_flag=True, default=False)
def web(debug):
    """Twitter Wall running as web server"""
    global twitter
    app.run(debug=debug)


def signal_handler(sig, frame):
    global wall
    wall.print_bye('Bye! See you soon...')
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    cli()
