import pytest
import betamax
import flexmock
from betamax.cassette import cassette
import os
import gzip
import base64
import json
import flask_injector
import injector
from twitterwall.common import TwitterConnection


def sanitize_requests(interaction, current_cassette):
    headers = interaction.data['request']['headers']
    auth = headers.get('Authorization')[0]
    if auth is None:
        return
    current_cassette.placeholders.append(
        cassette.Placeholder(placeholder='<AUTH>', replace=auth)
    )


def sanitize_responses(interaction, current_cassette):
    if interaction.data['response']['status']['code'] != 200:
        return
    data = interaction.as_response().json()
    if 'access_token' not in data:
        return
    print(interaction.as_response().json()['access_token'])
    interaction.as_response().json()['access_token'] = '<TOKEN>'
    print(interaction.as_response().json()['access_token'])
    new_data = base64.b64encode(gzip.compress('{"access_token":"<TOKEN>"}'.encode('ascii'))).decode('ascii')
    print(interaction.data['response']['body']['base64_string'])
    print(new_data)
    #interaction.data['response']['body']['base64_string'] = new_data
    current_cassette.placeholders.append(
        cassette.Placeholder(placeholder=new_data, replace=interaction.data['response']['body']['base64_string'])
    )  # this does not work... awesome! will spend few more hours on that


def sanitize_token(interaction, current_cassette):
    sanitize_requests(interaction, current_cassette)
    sanitize_responses(interaction, current_cassette)


with betamax.Betamax.configure() as config:
    config.cassette_library_dir = 'tests/fixtures/cassettes'
    if 'API_KEY' in os.environ and 'API_SECRET' in os.environ:
        config.default_cassette_options['record_mode'] = 'all'
    else:
        config.default_cassette_options['record_mode'] = 'none'
    config.before_record(callback=sanitize_token)


@pytest.fixture
def twitter(betamax_session):
    """TwitterConnection with betamax session"""
    api_key = os.environ.get('API_KEY', 'fake_key')
    api_secret = os.environ.get('API_SECRET', 'fake_secret')
    return TwitterConnection(api_key, api_secret, session=betamax_session)



@pytest.fixture
def twitter():
    from twitterwall.common import Tweet

    def get_tweets(params):
        with open('tests/fixtures/tweets.json') as f:
            return [Tweet(data) for data in json.load(f)['statuses']]
    return flexmock.flexmock(get_tweets=get_tweets)


@pytest.fixture
def webapp(twitter):
    from twitterwall.web import app

    def configure(binder):
        binder.bind(
            TwitterConnection,
            to=twitter,
            scope=injector.singleton
        )

    flask_injector.FlaskInjector(app=app, modules=[configure])

    app.config['TESTING'] = True
    app.config['AJAX_INTERVAL'] = 7
    app.config['INIT_COUNT'] = 10
    return app.test_client()
