import flask
import jinja2
import configparser
import json
from common import *

app = flask.Flask(__name__)
twitter = None


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/q/<query>')
@app.route('/q/<query>/<lang>')
def feed(query, lang=''):
    params = {'q': query, 'count': 10}
    if lang != '':
        params['lang'] = lang
    tweets = twitter.get_tweets(params)
    lid = tweets[0]['id']
    return flask.render_template('feed.html', query=query, lang=lang,
                                 tweets=reversed(tweets), lid=lid)


@app.route('/api/<lid>/<query>')
@app.route('/api/<lid>/<query>/<lang>')
def api(lid, query, lang=''):
    params = {'q': query, 'since_id': lid}
    if lang != '':
        params['lang'] = lang
    tweets = twitter.get_tweets(params)
    lid = tweets[0]['id']
    html = flask.render_template('tweets.html', tweets=reversed(tweets))
    return json.dumps({'lid':lid, 'html':html})


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


@app.template_filter('media_img')
def media_img(media):
    img = '<img src="{}" alt="{}" />'.format(
        media['media_url'],
        media['display_url']
    )
    link = '<a href="{}" target="_blank">{}</a>'.format(
        media['media_url'],
        img
    )
    return jinja2.Markup(link)


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


@app.template_filter('hashtags')
def hashtags(tweet):
    if 'hashtags' not in tweet['entities']:
        return 'none'
    res = [hashtag_link(h['text']) for h in tweet['entities']['hashtags']]
    return jinja2.Markup(', '.join(res))


@app.template_filter('mentions')
def mentions(tweet):
    if 'mentions' not in tweet['entities']:
        return 'none'
    res = [author_link(m['screen_name']) for m in
           tweet['entities']['user_mentions']]
    return jinja2.Markup(', '.join(res))


@app.template_filter('medias')
def medias(tweet):
    if 'media' not in tweet['entities']:
        return ''
    res = [media_img(m) for m in tweet['entities']['media']]
    return jinja2.Markup(' '.join(res))


def make_url_link(url):
    return '<a href="{}" target="_blank">{}</a>'.format(
        url['url'],
        url['display_url']
    )


@app.template_filter('urls')
def urls(tweet):
    if 'urls' not in tweet['entities']:
        return 'none'
    res = [make_url_link(u) for u in tweet['entities']['urls']]
    return jinja2.Markup(', '.join(res))


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
