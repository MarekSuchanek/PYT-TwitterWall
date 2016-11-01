from twitterwall.cli import *
from flexmock import flexmock


class FakePrinter:

    def clear(self):
        pass

    def echo(self, *args, **kwargs):
        pass

    def secho(self, *args, **kwargs):
        pass

    def style(self, str, *args, **kwargs):
        return str


def test_boring_wall(twitter_mock):
    tweet = twitter_mock.get_tweets({})[0]
    printer = flexmock(FakePrinter())
    printer.should_call('clear').once()
    printer.should_call('echo').at_least().once()

    wall = CLIWall(printer)
    wall.print_tweet(tweet)


def test_colorful_wall(twitter_mock):
    tweet = twitter_mock.get_tweets({})[0]
    printer = flexmock(FakePrinter())
    printer.should_call('clear').once()
    printer.should_call('secho').at_least().once()

    wall = CLIColorfulWall(printer)
    wall.print_tweet(tweet)


def test_colorful_wall_highlighter(twitter_mock):
    tweet = twitter_mock.get_tweets({})[0]
    printer = flexmock(FakePrinter())
    printer.should_call('style').at_least().once()

    wall = CLIColorfulWall(printer)
    wall.tweet_highlighter(tweet)


def text_tweetreader(twitter_mock):
    printer = flexmock(FakePrinter())
    printer.should_call('echo').at_least().twice()

    wall = CLIWall(printer)
    reader = TweetReader(twitter_mock, wall, '#python')
    reader.process_n(2)
