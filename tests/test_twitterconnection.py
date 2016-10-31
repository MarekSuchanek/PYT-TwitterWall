
def test_client_simple(twitter):
    assert len(twitter.get_tweets({'q': 'ahoj', 'count': 5})) <= 5
