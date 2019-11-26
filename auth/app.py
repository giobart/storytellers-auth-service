import os

from flask import Flask
from auth.views import blueprints
from auth.extensions import jwt
from flask_cors import CORS

__all__ = ('create_app',)

def create_app(config=None, app_name='auth'):
    '''
    Prepares initializes the application and its utilities.
    '''

    app = Flask(app_name)
    CORS(app)

    if config:
        app.config.from_pyfile(config)

    jwt.init_app(app)

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5005)
