import flask
import jinja2
import configparser
import json
from .common import TwitterConnection

app = flask.Flask(__name__)
twitter = None
cfg = {}


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/q/<query>')
@app.route('/q/<query>/<lang>')
def feed(query, lang=''):
    params = {'q': query, 'count': cfg['count'], 'include_entities': True}
    if lang != '':
        params['lang'] = lang
    tweets = twitter.get_tweets(params)
    lid = 0 if len(tweets) == 0 else tweets[-1]['id']
    return flask.render_template('feed.html', query=query, lang=lang,
                                 tweets=reversed(tweets), lid=lid,
                                 interval=cfg['interval'], count=len(tweets))


@app.route('/api/<lid>/<query>')
@app.route('/api/<lid>/<query>/<lang>')
def api(lid, query, lang=''):
    params = {'q': query, 'since_id': lid, 'include_entities': True}
    if lang != '':
        params['lang'] = lang
    tweets = twitter.get_tweets(params)
    if len(tweets) > 0:
        lid = tweets[-1]['id']
    res = [flask.render_template('tweet.html', tweet=t) for t in tweets]
    return json.dumps({'lid': lid, 'tweets': res})


@app.template_filter('author_avatar')
def author_avatar(tweet):
    return jinja2.Markup(
        '<img src="{}" alt="{}" class="avatar"/>'.format(
            tweet['user']['profile_image_url'],
            tweet.get_author_name()
        ))


@app.template_filter('author_link')
def user_link(screen_name):
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
def media_img(media, author, id):
    img = '<img src="{}" alt="{}" />'.format(
        media['media_url'], media['display_url']
    )
    link = '<a href="{}" target="_blank" ' \
           'data-lightbox="{}" data-title="@{} - {}">{}</a>'.format(
            media['media_url'], id, author, media['display_url'], img)
    return jinja2.Markup(link)


@app.template_filter('tweet_date')
def tweet_date(tweet):
    return tweet.get_created().strftime('%d/%m/%Y %H:%M:%S')


@app.template_filter('enhance_text')
def enhance_text(tweet):
    text = tweet.get_text()
    result = ""
    entities = []
    for hashtag in tweet.get_entities_of_type('hashtags'):
        entities.append(
            (hashtag['indices'][0], hashtag['indices'][1],
             hashtag_link(hashtag['text']))
        )
    for mention in tweet.get_entities_of_type('user_mentions'):
        entities.append(
            (mention['indices'][0], mention['indices'][1],
             user_link(mention['screen_name']))
        )
    for url in tweet.get_entities_of_type('urls'):
        entities.append(
            (url['indices'][0], url['indices'][1],
             url_link(url))
        )
    entities.sort(reverse=True)
    index = 0
    while len(entities) > 0:
        act = entities.pop()
        result += jinja2.Markup(text[index:act[0]]) + act[2]
        index = act[1]
    result += jinja2.Markup(text[index:])
    return result


@app.template_filter('hashtags')
def hashtags(tweet):
    res = [hashtag_link(h['text']) for h in
           tweet.get_entities_of_type('hashtags')]
    return jinja2.Markup(', '.join(res))


@app.template_filter('mentions')
def mentions(tweet):
    res = [user_link(m['screen_name']) for m in
           tweet.get_entities_of_type('user_mentions')]
    return jinja2.Markup(', '.join(res))


@app.template_filter('medias')
def medias(tweet):
    res = [media_img(m, tweet.get_author_nick(), tweet['id'])
           for m in tweet.get_entities_of_type('media')]
    return jinja2.Markup(' '.join(res))


@app.template_filter('url_link')
def url_link(url):
    return jinja2.Markup('<a href="{}" target="_blank">{}</a>'.format(
        url['url'],
        url['display_url']
    ))


@app.template_filter('urls')
def urls(tweet):
    res = [url_link(u) for u in tweet.get_entities_of_type('urls')]
    return jinja2.Markup(', '.join(res))


def start_web(debug, count, interval, tw):
    global twitter, cfg
    cfg = {'count': count, 'interval': interval}
    twitter = tw
    app.config['TEMPLATES_AUTO_RELOAD'] = debug
    app.run(debug=debug)


if __name__ == '__main__':
    authcfg = configparser.ConfigParser()
    authcfg.read('config/auth.cfg')
    twitter = TwitterConnection(authcfg['twitter']['key'],
                                authcfg['twitter']['secret'])
    start_web(True, 5, 3, twitter)
