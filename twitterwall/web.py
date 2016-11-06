import flask
import jinja2
import flask_injector
import injector
import json
from .common import TwitterConnection

app = flask.Flask(__name__)


@app.route('/')
def index():
    """Landing page with static content"""
    return flask.render_template('index.html')


@app.route('/q/<query>')
@app.route('/q/<query>/<lang>')
@injector.inject(twitter=TwitterConnection)
def feed(twitter, query, lang=''):
    """Feed page displaying tweets by given query (and lang)"""
    params = {
        'q': query,
        'count': app.config['INIT_COUNT'],
        'include_entities': True
    }
    if lang != '':
        params['lang'] = lang
    tweets = twitter.get_tweets(params)
    lid = 0 if len(tweets) == 0 else tweets[-1]['id']
    return flask.render_template('feed.html', query=query, lang=lang,
                                 tweets=reversed(tweets), lid=lid,
                                 interval=app.config['AJAX_INTERVAL'],
                                 count=len(tweets))


@app.route('/api/<lid>/<query>')
@app.route('/api/<lid>/<query>/<lang>')
@injector.inject(twitter=TwitterConnection)
def api(twitter, lid, query, lang=''):
    """API url for providing tweets by AJAX"""
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
    """Filter to show author avatar from tweet"""
    return jinja2.Markup(
        '<img src="{}" alt="{}" class="avatar"/>'.format(
            tweet['user']['profile_image_url'],
            tweet.get_author_name()
        ))


@app.template_filter('author_link')
def user_link(screen_name):
    """Filter to show user link from username"""
    return jinja2.Markup(
        '<a href="{}" target="_blank">@{}</a>'.format(
            'https://twitter.com/{}'.format(screen_name),
            screen_name
        ))


@app.template_filter('hashtag_link')
def hashtag_link(hashtag):
    """Filter to show link from hashtag"""
    return jinja2.Markup(
        '<a href="{}" target="_blank">#{}</a>'.format(
            'https://twitter.com/hashtag/{}'.format(hashtag),
            hashtag
        ))


@app.template_filter('media_img')
def media_img(media, author, id):
    """Filter to show img media via lightbox with caption"""
    img = '<img src="{}" alt="{}" />'.format(
        media['media_url'], media['display_url']
    )
    link = '<a href="{}" target="_blank" ' \
           'data-lightbox="{}" data-title="@{} - {}">{}</a>'.format(
            media['media_url'], id, author, media['display_url'], img)
    return jinja2.Markup(link)


@app.template_filter('tweet_date')
def tweet_date(tweet):
    """Filter to format tweet created datetime"""
    return tweet.get_created().strftime('%d/%m/%Y %H:%M:%S')


@app.template_filter('enhance_text')
def enhance_text(tweet):
    """Filter to make URLs for entities in the text of tweet"""
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
    """Filter to show list of hashtags from tweet"""
    res = [hashtag_link(h['text']) for h in
           tweet.get_entities_of_type('hashtags')]
    return jinja2.Markup(', '.join(res))


@app.template_filter('mentions')
def mentions(tweet):
    """Filter to show list of user mentions from tweet"""
    res = [user_link(m['screen_name']) for m in
           tweet.get_entities_of_type('user_mentions')]
    return jinja2.Markup(', '.join(res))


@app.template_filter('medias')
def medias(tweet):
    """Filter to show list of medias from tweet"""
    res = [media_img(m, tweet.get_author_nick(), tweet['id'])
           for m in tweet.get_entities_of_type('media')]
    return jinja2.Markup(' '.join(res))


@app.template_filter('url_link')
def url_link(url):
    """Filter to show url link from url"""
    return jinja2.Markup('<a href="{}" target="_blank">{}</a>'.format(
        url['url'],
        url['display_url']
    ))


@app.template_filter('urls')
def urls(tweet):
    """Filter to show list of URLs from tweet"""
    res = [url_link(u) for u in tweet.get_entities_of_type('urls')]
    return jinja2.Markup(', '.join(res))


def configure(binder):
    """Configure injector binding"""
    binder.bind(
        TwitterConnection,
        to=TwitterConnection(
            app.config['API_KEY'],
            app.config['API_SECRET']
        ),
        scope=injector.singleton
    )


def init_injector():
    """Start Flask injector for web app"""
    flask_injector.FlaskInjector(app=app, modules=[configure])
