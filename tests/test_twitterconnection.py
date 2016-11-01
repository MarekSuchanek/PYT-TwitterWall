import pytest
import itertools
from datetime import datetime


@pytest.mark.parametrize('count', [1, 3, 5, 10])
def test_client_simple(twitter, count):
    assert len(twitter.get_tweets({'q': '#python', 'count': count})) <= count


@pytest.mark.parametrize(
    ['query', 'count'],
    itertools.product(['have', '#python'], [1, 5, 7])
)
def test_client_query(twitter, query, count):
    tweets = twitter.get_tweets({'q': query, 'count': count, 'lang': 'en'})
    assert len(tweets) <= count
    for tweet in tweets:
        assert query in tweet.get_text().lower()


@pytest.mark.parametrize(
    ['query', 'count'],
    itertools.product(['have', '#python'], [1, 5, 7])
)
def test_client_query(twitter, query, count):
    tweets = twitter.get_tweets({'q': query, 'count': count, 'lang': 'en'})
    assert len(tweets) <= count
    for tweet in tweets:
        assert query in tweet.get_text().lower()


@pytest.mark.parametrize(
    ['query', 'max_id', 'count'],
    zip(
        ['#python', '#python'],
        [793480517928779781, 693480517928779781],
        [10, 10]
    )
)
def test_client_max_id(twitter, query, max_id, count):
    tweets = twitter.get_tweets(
        {'q': query, 'count': count, 'max_id': max_id}
    )
    for tweet in tweets:
        assert tweet.get_id() <= max_id


@pytest.mark.parametrize(
    ['query', 'since_id', 'count'],
    zip(
        ['#python', '#python'],
        [793480517928779781, 693480517928779781],
        [10, 10]
    )
)
def test_client_since_id(twitter, query, since_id, count):
    tweets = twitter.get_tweets(
        {'q': query, 'count': count, 'since_id': since_id}
    )
    for tweet in tweets:
        assert tweet.get_id() > since_id


@pytest.mark.parametrize(
    ['query', 'until', 'count'],
    zip(
        ['#python', '#python'],
        [datetime(2016, 1, 1), datetime(2015, 5, 15)],
        [10, 10]
    )
)
def test_client_until(twitter, query, until, count):
    tweets = twitter.get_tweets(
        {'q': query, 'count': count, 'until': until.strftime('%Y-%m-%d')}
    )
    for tweet in tweets:
        assert tweet.get_created() < until
