Flask filters examples
======================

You can use `Flask filters`_ defined in ``twitterwall.web`` module
so you can use them to show Tweet and it's parts in web page.

.. _Flask filters: http://flask.pocoo.org/docs/0.11/templating/#registering-filters


.. testsetup::

    from twitterwall.common import Tweet
    from twitterwall.web import *
    from jinja2 import Markup
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

For Tweet object ``Tweet(jsondata)`` (same data as in :doc:`tweet`), you can use for example:

.. doctest::

    >>> author_avatar(tweet)
    Markup('<img src="http://a0.twimg.com/profile_images/2359746665/1v6zfgqo8g0d3mk7ii5s_normal.jpeg" alt="Sean Cummings" class="avatar"/>')
    >>> tweet_date(tweet)
    '24/09/2012 03:35:21'
    >>> enhance_text(tweet)
    Markup('Aggressive Ponytail <a href="https://twitter.com/hashtag/freebandnames" target="_blank">#freebandnames</a>')
    >>> hashtags(tweet)
    Markup('<a href="https://twitter.com/hashtag/freebandnames" target="_blank">#freebandnames</a>')
    >>> mentions(tweet)
    Markup('')
    >>> urls(tweet)
    Markup('')

There are also some filters to other things than whole Tweet object, for example:

.. doctest::

    >>> user_link('andy123')
    Markup('<a href="https://twitter.com/andy123" target="_blank">@andy123</a>')
    >>> hashtag_link('python')
    Markup('<a href="https://twitter.com/hashtag/python" target="_blank">#python</a>')

String are markup'ed by ``jinja2.Markup``.
