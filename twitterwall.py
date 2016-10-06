import configparser
import time
import base64
import requests
import click

tweet_api_url = 'https://api.twitter.com/1.1/search/tweets.json'


def twitter_session(conf_file):
    config = configparser.ConfigParser()
    config.read(conf_file)
    api_key = config['twitter']['key']
    api_secret = config['twitter']['secret']

    session = requests.Session()
    secret = '{}:{}'.format(api_key, api_secret)
    secret64 = base64.b64encode(secret.encode('ascii')).decode('ascii')

    headers = {
        'Authorization': 'Basic {}'.format(secret64),
        'Host': 'api.twitter.com',
    }

    r = session.post('https://api.twitter.com/oauth2/token',
                     headers=headers,
                     data={'grant_type': 'client_credentials'})

    bearer_token = r.json()['access_token']

    def bearer_auth(req):
        req.headers['Authorization'] = 'Bearer ' + bearer_token
        return req

    session.auth = bearer_auth
    return session


def print_tweet(tweet):
    click.echo('## '+tweet['created_at'])
    click.secho(tweet['user']['name'], bold=True, fg='blue', nl=False)
    click.echo(': '+tweet['text'])
    click.echo()


def get_tweets(session, params):
    r = session.get(tweet_api_url, params=params)
    return reversed(r.json()['statuses'])


def tweets_process(session, params):
    last_id = 0
    for t in get_tweets(session, params):
        if t['id'] > last_id:
            last_id = t['id']
        print_tweet(t)
    return last_id


@click.command()
@click.option('--config', default="auth.cfg", help='App config file path.')
@click.option('--expr', prompt='Filter', help='Expression to filter tweets.')
@click.option('--count', default=5, help='Number of initial tweets.')
@click.option('--interval', default=10, help='Seconds to check new tweets.')
def twitter_wall(config, expr, count, interval):
    '''Simple Twitter Wall for loading desired tweets in CLI'''
    session = twitter_session(config)
    params = {'q': expr, 'count': count}

    click.clear()

    last_id = tweets_process(session, params)
    del params['count']
    while True:
        time.sleep(interval)
        params['since_id'] = last_id
        last_id = tweets_process(session, params)


if __name__ == '__main__':
    twitter_wall()
