import pytest
import betamax
from betamax.cassette import cassette
import os
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
    url = interaction.data['response']['url']
    auth = interaction.data['response']['body'].get('base64_string')
    if 'oauth2/token' not in url or auth is None:
        return
    current_cassette.placeholders.append(
        cassette.Placeholder(placeholder='<TOKEN>', replace=auth)
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
