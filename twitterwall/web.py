import flask
import jinja2
import configparser
from common import *

app = flask.Flask(__name__)
twitter = None


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/<query>')
@app.route('/<query>/<lang>')
def feed(query=None, lang=None):
    tweets = twitter.get_tweets({'q': query, 'count': 10})
    return flask.render_template('feed.html', query=query,
                                 tweets=reversed(tweets))


@app.template_filter('author_avatar')
def author_avatar(tweet):
    return jinja2.Markup(
        '<img src="{}" alt="{}" class="avatar"/>'.format(
            tweet['user']['profile_image_url'],
            tweet.get_author_name()
        ))


@app.template_filter('author_link')
def author_link(screen_name):
    return jinja2.Markup(
        '<a href="{}" target="_blank">@{}</a>'.format(
            'https://twitter.com/{}'.format(screen_name),
            screen_name
        ))


@app.template_filter('hashtag_link')
def hashtag_link(hashtag):
    return jinja2.Markup(
        '<a href="{}" target="_blank">#{}</a>'.format(
            'https://twitter.com/hashtag/{}'.format(hashtag),
            hashtag
        ))


@app.template_filter('tweet_date')
def tweet_date(tweet):
    return tweet.get_created().strftime('%d/%m/%Y %H:%M:%S')


@app.template_filter('enhance_text')
def enhance_text(tweet):
    words = tweet.get_text().split(' ')
    for i, w in enumerate(words):
        if Tweet.is_hashtag(w):
            words[i] = '<a href="{}" target="_blank">{}</a>'.format(
                'https://twitter.com/hashtag/{}'.format(w[1:]),
                w
            )
        elif Tweet.is_mention(w):
            words[i] = author_link(w[1:])
        elif Tweet.is_hyperref(w):
            words[i] = '<a href="{}" target="_blank">{}</a>'.format(w, w)
    return jinja2.Markup(' '.join(words))


@app.template_filter('enhance_text')
def hashtags(tweet):
    words = tweet.get_text().split(' ')
    for i, w in enumerate(words):
        if Tweet.is_hashtag(w):
            words[i] = hashtag_link(w[1:])
        elif Tweet.is_mention(w):
            words[i] = author_link(w[1:])
        elif Tweet.is_hyperref(w):
            words[i] = '<a href="{}" target="_blank">{}</a>'.format(w, w)
    return jinja2.Markup(' '.join(words))


def start_web(debug, tw):
    global twitter
    twitter = tw
    app.config['TEMPLATES_AUTO_RELOAD'] = debug
    app.run(debug=debug)

if __name__ == '__main__':
    authcfg = configparser.ConfigParser()
    authcfg.read('config/auth.cfg')
    twitter = TwitterConnection(authcfg['twitter']['key'],
                                authcfg['twitter']['secret'])
    start_web(True, twitter)
