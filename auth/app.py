import os

from flask import Flask
from flask_jwt_extended import JWTManager
from auth.views import blueprints
import auth

app = Flask(__name__)

# BASE URL FOR USERS SERVICE, USED ONLY IF USERS_API_URL ENVIRONMENT VARIABLE IS NOT SET
USERS_BASE_URL = "http://127.0.0.1"


def create_app():
    '''
    Prepares initializes the application and its utilities.
    '''

    # JWT TOKEN CONFIGURATION
    app.config['SECRET_KEY'] = 'some-secret-string-CHANGE-ME'
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string-CHANGE-ME'
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
    app.config['JWT_REFRESH_COOKIE_PATH'] = '/auth/token_refresh'

    # SET URL OF THE USERS SERVICE
    if os.environ.get('USERS_API'):
        auth.api_config['USERS_BASE_URL'] = os.environ.get('USERS_API')
    else:
        auth.api_config['USERS_BASE_URL'] = USERS_BASE_URL

    print("USERS_URL = " + auth.api_config['USERS_BASE_URL'])

    # Set True in production environment, False only for debugging purpose
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False

    # Only allow JWT cookies to be sent over https. In production, this
    # should likely be True
    app.config['JWT_COOKIE_SECURE'] = False

    jwt = JWTManager(app)

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0')
