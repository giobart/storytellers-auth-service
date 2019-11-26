from auth.app import create_app
from unittest.mock import patch, Mock
import pytest
from auth.app import create_app


@pytest.fixture
def app():
    '''
    Builds and configures a new app instance for each test
    Automatically manages the temporary files.
    '''

    app = create_app(config='tests/config_test.py')
    yield app


@pytest.fixture()
def client_factory(app):

    class ClientFactory:

        def __init__(self, app):
            self._app = app

        def get(self):
            return self._app.test_client()

    return ClientFactory(app)


@pytest.fixture()
def client(app, client_factory):
    return client_factory.get()


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
