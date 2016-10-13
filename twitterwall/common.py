import time
import base64
from datetime import datetime
import requests


class TwitterConnection:
    tweet_api_url = 'https://api.twitter.com/1.1/search/tweets.json'
    timeout = 5

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = self.start_session()

    def start_session(self):
        session = requests.Session()
        secret = '{}:{}'.format(self.api_key, self.api_secret)
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

    @staticmethod
    def is_hashtag(word):
        return word.startswith('#')

    @staticmethod
    def is_mention(word):
        return word.startswith('@')

    @staticmethod
    def is_hyperref(word):
        return word.startswith('https://') or \
               word.startswith('http://')


class TweetReader:

    def __init__(self, twitter, wall, query, lang):
        self.twitter = twitter
        self.wall = wall
        self.params = {'q': query, 'since_id': 0}
        self.tf = {}
        if lang is not None:
            self.params['lang'] = lang

    def setup_filter(self, no_rt, rt_min, rt_max, f_min,
                     f_max, authors, bauthors):
        authors = {a.lower() for a in authors}
        bauthors = {ba.lower() for ba in bauthors}
        self.tf = {}
        if no_rt:
            self.tf['rt'] = lambda t: not t.is_retweet()

        if rt_max is not None:
            self.tf['rt_count'] = lambda t: rt_min < t.get_nretweets() < rt_max
        elif rt_min > 0:
            self.tf['rt_count'] = lambda t: rt_min < t.get_nretweets()

        if f_max is not None:
            self.tf['user_f'] = lambda t: f_min < t.get_nfollows() < f_max
        elif f_min > 0:
            self.tf['user_f'] = lambda t: f_min < t.get_nfollows()

        if len(authors) > 0:
            self.tf['user_a'] = \
                lambda t: t.get_author_nick().lower() in authors

        if len(bauthors) > 0:
            self.tf['user_b'] = \
                lambda t: t.get_author_nick().lower() not in bauthors

        return self.tf

    def process_n(self, n):
        self.params['count'] = n
        self.process_periodic()
        del self.params['count']

    def process_periodic(self):
        for t in self.twitter.get_tweets(self.params):
            if t.get_id() > self.params['since_id']:
                self.params['since_id'] = t.get_id()
            if self.tweet_filter(t):
                self.wall.print_tweet(t)

    def tweet_filter(self, tweet):
        for rule in self.tf:
            if not self.tf[rule](tweet):
                return False
        return True

    def run(self, init_cnt, interval):
        self.process_n(init_cnt)
        while True:
            time.sleep(interval)
            self.process_periodic()