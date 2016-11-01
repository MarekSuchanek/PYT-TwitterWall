from twitterwall.web import *


def test_mock_landing(webapp):
    assert webapp.get('/').status == '200 OK'
    assert '<h1>Twitter Wall</h1>' in \
           webapp.get('/').data.decode('utf-8')


def test_mock_feed_simple(webapp):
    assert webapp.get('/q/yolo').status == '200 OK'
    assert 'yolo' in webapp.get('/q/yolo').data.decode('utf-8')


def test_mock_feed_with_lang(webapp):
    assert webapp.get('/q/yolo/cs').status == '200 OK'
    assert 'yolo' in webapp.get('/q/yolo/cs').data.decode('utf-8')


def test_mock_api_simple(webapp):
    assert webapp.get('/api/0/yolo').status == '200 OK'
    assert 'tweet' in webapp.get('/api/0/yolo').data.decode('utf-8')


def test_mock_api_with_lang(webapp):
    assert webapp.get('/api/0/yolo/cs').status == '200 OK'
    assert 'tweet' in webapp.get('/api/0/yolo/cs').data.decode('utf-8')


def test_author_avatar(twitter_mock):
    tweet = twitter_mock.get_tweets({})[0]
    result = author_avatar(tweet)
    assert 'img' in result
    assert tweet['user']['profile_image_url'] in result


def test_user_link():
    result = user_link('troll123')
    assert 'a href' in result
    assert 'troll123' in result


def test_hashtag_link():
    result = hashtag_link('hate')
    assert 'a href' in result
    assert '#hate' in result
    assert 'twitter.com/hashtag/hate' in result


def test_media_img():
    result = media_img(
        {'media_url': 'nope.jpg', 'display_url': 'nope.jpg'},
        'troll123', '1234'
    )
    assert 'img' in result
    assert 'a href' in result
    assert 'nope.jpg' in result


def test_tweet_date(twitter_mock):
    tweet = twitter_mock.get_tweets({})[0]
    result = tweet_date(tweet)
    assert str(tweet.get_created().day) in result
    assert str(tweet.get_created().month) in result
    assert str(tweet.get_created().year) in result
    assert str(tweet.get_created().hour) in result
    assert str(tweet.get_created().minute) in result
    assert str(tweet.get_created().second) in result


def test_enhance_text(twitter_mock):
    tweet = twitter_mock.get_tweets({})[0]
    tweet['entities']['hashtags'] = [
          {
              "text": "freebandnames",
              "indices": [20, 34]
          }
        ]
    tweet['entities']['user_mentions'] = [{
      "screen_name": "TwitterEng",
      "name": "Twitter Engineering",
      "id": 6844292,
      "id_str": "6844292",
      "indices": [81, 92]
    }]
    tweet['entities']['urls'] = [{
      "url": "https://t.co/XdXRudPXH5",
      "expanded_url": "https://blog.twitter.com/2013/rich-photo",
      "display_url": "blog.twitter.com/2013/rich-phot\u2026",
      "indices": [80, 103]
    }]
    result = enhance_text(tweet)
    assert 'a href' in result


def test_hashtags(twitter_mock):
    tweet = twitter_mock.get_tweets({})[0]
    tweet['entities']['hashtags'] = [
          {
              "text": "freebandnames",
              "indices": [20, 34]
          }
        ]
    assert 'freebandnames' in hashtags(tweet)


def test_mentions(twitter_mock):
    tweet = twitter_mock.get_tweets({})[0]
    tweet['entities']['user_mentions'] = [{
      "screen_name": "TwitterEng",
      "name": "Twitter Engineering",
      "id": 6844292,
      "id_str": "6844292",
      "indices": [81, 92]
    }]
    assert 'TwitterEng' in mentions(tweet)


def test_medias(twitter_mock):
    tweet = twitter_mock.get_tweets({})[0]
    tweet['entities']['media'] = [{
      "id": 266031293949698048,
      "id_str": "266031293949698048",
      "indices": [17, 37],
      "media_url": "http://pbs.twimg.com/media/A7EiDWcCYAAZT1D.jpg",
      "media_url_https": "https://pbs.twimg.com/media/A7EiDWcCYAAZT1D.jpg",
      "url": "http://t.co/bAJE6Vom",
      "display_url": "pic.twitter.com/bAJE6Vom",
      "expanded_url": "http://twitter.com/nub/status/0000/photo/1",
      "type": "photo",
      "sizes": {}
    }]
    assert tweet['entities']['media'][0]['media_url'] in medias(tweet)


def test_urls(twitter_mock):
    tweet = twitter_mock.get_tweets({})[0]
    tweet['entities']['urls'] = [{
      "url": "https://t.co/XdXRudPXH5",
      "expanded_url": "https://blog.twitter.com/2013/rich-photo",
      "display_url": "blog.twitter.com/2013/rich-phot\u2026",
      "indices": [80, 103]
    }]
    assert tweet['entities']['urls'][0]['url'] in urls(tweet)


def test_url_link():
    url = {
      "url": "https://t.co/XdXRudPXH5",
      "expanded_url": "https://blog.twitter.com/2013/rich-photo",
      "display_url": "blog.twitter.com/2013/rich-phot\u2026",
      "indices": [80, 103]
    }
    result = url_link(url)
    assert url['url'] in result
    assert 'a href' in result
