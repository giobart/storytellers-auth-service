from auth.app import create_app
from unittest.mock import patch, Mock
import pytest


@pytest.fixture
def app():
    '''
    Builds and configures a new app instance for each test
    Automatically manages the temporary files.
    '''

    app = create_app()
    yield app


class ClientFactory:

    def __init__(self, app):
        self._app = app

    def get(self):
        return self._app.test_client()


@pytest.fixture
def client_factory(app):
    return ClientFactory(app)


@pytest.fixture
def client(app, client_factory):
    '''
    Builds a new test client instance.
    '''
    return client_factory.get()


@pytest.fixture
def mock_login_user():
    mock_login_user_patcher = patch('auth.utility.api_call.requests.post')

    mock = mock_login_user_patcher.start()

    return mock
