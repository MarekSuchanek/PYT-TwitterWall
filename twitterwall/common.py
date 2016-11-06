import base64
from datetime import datetime
import requests


class TwitterConnection:
    """
    Twitter API client for searching tweets

    :cvar timeout: Requests timeout in seconds
    :cvar tweet_api_url: API URL for searching tweets
    :ivar session: Twitter authorized session (connection)

    """
    timeout = 5
    tweet_api_url = 'https://api.twitter.com/1.1/search/tweets.json'

    def __init__(self, api_key, api_secret, session=None):
        """
        Start client by setting up the session for communication
        with Twitter API
        """
        self.session = session or requests.Session()
        self._start_session(api_key, api_secret)

    def _start_session(self, api_key, api_secret):
        """Start authorized session with Twitter API"""
        secret = '{}:{}'.format(api_key, api_secret)
        secret64 = base64.b64encode(secret.encode('ascii')).decode('ascii')

        headers = {
            'Authorization': 'Basic {}'.format(secret64),
            'Host': 'api.twitter.com',
        }

        r = self.session.post('https://api.twitter.com/oauth2/token',
                              headers=headers,
                              data={'grant_type': 'client_credentials'},
                              timeout=self.timeout)
        r.raise_for_status()

        bearer_token = r.json()['access_token']

        def bearer_auth(req):
            req.headers['Authorization'] = 'Bearer ' + bearer_token
            return req

        self.session.auth = bearer_auth

    def get_tweets(self, params):
        """Request and return tweets from Twitter API with given params"""
        r = self.session.get(self.tweet_api_url,
                             params=params,
                             timeout=self.timeout)
        r.raise_for_status()
        return [Tweet(t) for t in reversed(r.json()['statuses'])]


class Tweet:
    """
    Twitter tweet data wrapper concentrating getters

    :cvar dformat: Twitter's tweet datetime format
    :cvar tweet_url: Tweet URL template (need to fill author and ID)
    :ivar data: Wrapper tweet data from JSON

    """
    dformat = '%a %b %d %H:%M:%S +0000 %Y'
    tweet_url = 'https://twitter.com/{}/statuses/{}'

    def __init__(self, jsondata):
        """Construct new Tweet by providing data from JSON"""
        self.data = jsondata

    def __getitem__(self, key):
        """Get item directly from wrapped data"""
        return self.data[key]

    def __setitem__(self, key, value):
        """Set value to item directly from wrapped data"""
        self.data[key] = value

    def get_id(self):
        """Get tweet ID"""
        return self.data['id']

    def get_text(self):
        """Get full text of the tweet"""
        return self.data['text']

    def get_nretweets(self):
        """Get number of retweets of tweet"""
        return self.data['retweet_count']

    def get_author_name(self):
        """Get full name of author of tweet"""
        return self.data['user']['name']

    def get_author_nick(self):
        """Get nick (username) of author of tweet"""
        return self.data['user']['screen_name']

    def get_nfollows(self):
        """Get number of followers of author of tweet"""
        return self.data['user']['followers_count']

    def get_created(self):
        """Get datetime when tweet was created"""
        return datetime.strptime(self.data['created_at'],
                                 self.dformat)

    def get_url(self):
        """Get url of tweet"""
        return self.tweet_url.format(self.get_author_nick(), self.get_id())

    def is_retweet(self):
        """Check if this tweet is just retweet of another tweet"""
        return 'retweeted_status' in self.data

    def get_entities_of_type(self, type):
        """Get list of tweet entities of desired type"""
        return self.data.get('entities', {}).get(type, [])
