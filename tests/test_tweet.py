import pytest
import itertools
from datetime import datetime
from twitterwall.common import Tweet


various_values = ['String', -5, None, True, 10.5, {'x': 7}]
names = ['Roy', 'Maurice', 'Richmond', 'Jen', 'Peter File']
nicks = ['sloth', 'gluttony', 'lust', 'pride', 'greed', 'wrath', 'envy']
ints = range(0, 5000, 107)
entity_types = ['media', 'urls', 'usermentions', 'hashtags', 'symbols']


@pytest.mark.parametrize(
    ['attr', 'val'],
    itertools.product(nicks, various_values)
)
def test_get(attr, val):
    tweet = Tweet({attr: val})
    assert tweet[attr] == val


@pytest.mark.parametrize(
    ['attr', 'val1', 'val2'],
    itertools.product(nicks, various_values, various_values)
)
def test_set(attr, val1, val2):
    tweet = Tweet({attr: val1})
    tweet[attr] = val2
    assert tweet[attr] == val2


@pytest.mark.parametrize('id', ints)
def test_get_id(id):
    tweet = Tweet({'id': id})
    assert tweet.get_id() == id


@pytest.mark.parametrize('text', names)
def test_get_text(text):
    tweet = Tweet({'text': text})
    assert tweet.get_text() == text


@pytest.mark.parametrize('cnt', ints)
def test_get_nretweets(cnt):
    tweet = Tweet({'retweet_count': cnt})
    assert tweet.get_nretweets() == cnt


@pytest.mark.parametrize('name', names)
def test_get_author_name(name):
    tweet = Tweet({'user': {'name': name}})
    assert tweet.get_author_name() == name


@pytest.mark.parametrize('nick', nicks)
def test_get_author_nick(nick):
    tweet = Tweet({'user': {'screen_name': nick}})
    assert tweet.get_author_nick() == nick


@pytest.mark.parametrize('cnt', ints)
def test_get_nfollows(cnt):
    tweet = Tweet({'user': {'followers_count': cnt}})
    assert tweet.get_nfollows() == cnt


@pytest.mark.parametrize(
    ['year', 'month', 'day', 'hour', 'min', 'sec'],
    itertools.product(
        [2016],
        [1, 5, 12],
        [7, 25],
        [0, 13, 23],
        [0, 18, 59],
        [0, 18, 59],
    )
)
def test_get_created(year, month, day, hour, min, sec):
    dt = datetime(year, month, day, hour, min, sec)
    tweet = Tweet({'created_at': dt.strftime(Tweet.dformat)})
    assert tweet.get_created() == dt


@pytest.mark.parametrize(
    ['nick', 'id'],
    itertools.product(nicks, ints)
)
def test_get_url(nick, id):
    tweet = Tweet({'id': id, 'user': {'screen_name': nick}})
    assert tweet.get_url() == tweet.tweet_url.format(nick, id)


@pytest.mark.parametrize('id', ints)
def test_is_retweet(id):
    tweet = Tweet({'retweeted_status': id})
    assert tweet.is_retweet()


def test_is_retweet_neg():
    tweet = Tweet({'id': 123456})
    assert not tweet.is_retweet()


@pytest.mark.parametrize('type', entity_types)
def test_get_entities_of_type(type):
    ents = ['a', 'b', 'c']
    tweet = Tweet({'entities': {type: ents}})
    assert tweet.get_entities_of_type(type) is ents
