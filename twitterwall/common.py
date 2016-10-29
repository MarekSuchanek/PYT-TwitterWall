import base64
from datetime import datetime
import requests


class TwitterConnection:
    tweet_api_url = 'https://api.twitter.com/1.1/search/tweets.json'
    timeout = 5

    def __init__(self, api_key, api_secret, session=None):
        self.session = session
        if session is None:
            self.session = self._start_session(api_key, api_secret)

    def _start_session(self, api_key, api_secret):
        session = requests.Session()
        secret = '{}:{}'.format(api_key, api_secret)
        secret64 = base64.b64encode(secret.encode('ascii')).decode('ascii')

        headers = {
            'Authorization': 'Basic {}'.format(secret64),
            'Host': 'api.twitter.com',
        }

        r = session.post('https://api.twitter.com/oauth2/token',
                         headers=headers,
                         data={'grant_type': 'client_credentials'},
                         timeout=self.timeout)
        r.raise_for_status()

        bearer_token = r.json()['access_token']

        def bearer_auth(req):
            req.headers['Authorization'] = 'Bearer ' + bearer_token
            return req

        session.auth = bearer_auth
        return session

    def get_tweets(self, params):
        r = self.session.get(self.tweet_api_url,
                             params=params,
                             timeout=self.timeout)
        r.raise_for_status()
        return [Tweet(t) for t in reversed(r.json()['statuses'])]


class Tweet:
    """Twitter tweet data wrapper concentrating getters"""
    dformat = '%a %b %d %H:%M:%S +0000 %Y'

    def __init__(self, jsondata):
        self.data = jsondata

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    def get_id(self):
        return self.data['id']

    def get_text(self):
        return self.data['text']

    def get_nretweets(self):
        return self.data['retweet_count']

    def get_author_name(self):
        return self.data['user']['name']

    def get_author_nick(self):
        return self.data['user']['screen_name']

    def get_nfollows(self):
        return self.data['user']['followers_count']

    def get_created(self):
        return datetime.strptime(self.data['created_at'],
                                 self.dformat)

    def get_url(self):
        return 'https://twitter.com/{}/statuses/{}'.\
            format(self.get_author_nick(), self.get_id())

    def is_retweet(self):
        return 'retweeted_status' in self.data

    def get_entities_of_type(self, type):
        return self.data.get('entities', {}).get(type, [])
