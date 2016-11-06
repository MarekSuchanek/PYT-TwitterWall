Tweet examples
==============

Let's say we got following JSON coming up as tweet
from Twitter API (simplified example from `API docs`_):

::

  {
      "created_at": "Mon Sep 24 03:35:21 +0000 2012",
      "id_str": "250075927172759552",
      "entities": {
        "urls": [],
        "hashtags": [
          {
            "text": "freebandnames",
            "indices": [20, 34]
          }
        ],
        "user_mentions": []
      },
      "text": "Aggressive Ponytail #freebandnames",
      "retweet_count": 0,
      "id": 250075927172759552,
      "retweeted": false,
      "user": {
        "name": "Sean Cummings",
        "profile_image_url": "http://a0.twimg.com/profile_images/2359746665/1v6zfgqo8g0d3mk7ii5s_normal.jpeg",
        "created_at": "Mon Apr 26 06:01:55 +0000 2010",
        "location": "LA, CA",
        "profile_image_url_https": "https://si0.twimg.com/profile_images/2359746665/1v6zfgqo8g0d3mk7ii5s_normal.jpeg",
        "id": 137238150,
        "followers_count": 70,
        "verified": false,
        "time_zone": "Pacific Time (US & Canada)",
        "description": "Born 330 Live 310",
        "profile_background_image_url": "http://a0.twimg.com/images/themes/theme1/bg.png",
        "statuses_count": 579,
        "friends_count": 110,
        "screen_name": "sean_cummings"
      },
      "source": "Twitter for Mac"
    }


.. testsetup::

    from twitterwall.common import Tweet
    import datetime
    tweet = Tweet({
      "created_at": "Mon Sep 24 03:35:21 +0000 2012",
      "id_str": "250075927172759552",
      "entities": {
        "urls": [],
        "hashtags": [
          {
            "text": "freebandnames",
            "indices": [20, 34]
          }
        ],
        "user_mentions": []
      },
      "text": "Aggressive Ponytail #freebandnames",
      "retweet_count": 0,
      "id": 250075927172759552,
      "retweeted": False,
      "user": {
        "name": "Sean Cummings",
        "profile_image_url": "http://a0.twimg.com/profile_images/2359746665/1v6zfgqo8g0d3mk7ii5s_normal.jpeg",
        "created_at": "Mon Apr 26 06:01:55 +0000 2010",
        "location": "LA, CA",
        "profile_image_url_https": "https://si0.twimg.com/profile_images/2359746665/1v6zfgqo8g0d3mk7ii5s_normal.jpeg",
        "id": 137238150,
        "followers_count": 70,
        "verified": False,
        "time_zone": "Pacific Time (US & Canada)",
        "description": "Born 330 Live 310",
        "profile_background_image_url": "http://a0.twimg.com/images/themes/theme1/bg.png",
        "statuses_count": 579,
        "friends_count": 110,
        "screen_name": "sean_cummings"
      },
      "source": "Twitter for Mac"
    })

Tweet object ``Tweet(jsondata)`` serves as wrapper to those JSON data:

.. doctest::

    >>> tweet.get_id()
    250075927172759552
    >>> tweet.get_text()
    'Aggressive Ponytail #freebandnames'
    >>> tweet.get_nretweets()
    0
    >>> tweet.get_author_name()
    'Sean Cummings'
    >>> tweet.get_author_nick()
    'sean_cummings'
    >>> tweet.get_nfollows()
    70
    >>> tweet.get_created()
    datetime.datetime(2012, 9, 24, 3, 35, 21)
    >>> tweet.get_url()
    'https://twitter.com/sean_cummings/statuses/250075927172759552'
    >>> tweet.is_retweet()
    False
    >>> len(tweet.get_entities_of_type('hashtags'))
    1
    >>> tweet.get_entities_of_type('hashtags')[0]['text']
    'freebandnames'
    >>> tweet.get_entities_of_type('hashtags')[0]['indices']
    [20, 34]

.. _API docs: https://dev.twitter.com/rest/reference/get/search/tweets

