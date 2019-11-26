# -*- coding: utf-8 -*-
import os

SECRET_KEY = 'change me please'

# Upstream requests timeout in seconds
REQUESTS_TIMEOUT = 0.33

# Microservices endpoints
USERS_ENDPOINT = os.getenv('USERS_API', 'localhost:5001')
STORIES_ENDPOINT = os.getenv('STORIES_API', 'localhost:5002')
REACTIONS_ENDPOINT = os.getenv('REACTIONS_API', 'localhost:5003')
STATISTICS_ENDPOINT = os.getenv('STATISTICS_API', 'localhost:5004')
AUTH_ENDPOINT = os.getenv('AUTH_API', 'localhost:5005')

# JWT
SECRET_KEY = 'some-secret-string-CHANGE-ME'
JWT_SECRET_KEY = 'jwt-secret-string-CHANGE-ME'
JWT_TOKEN_LOCATION = ['cookies']
JWT_ACCESS_COOKIE_PATH = '/'
JWT_REFRESH_COOKIE_PATH = '/auth/token_refresh'
JWT_COOKIE_CSRF_PROTECT = False  # False for debug purpose
JWT_COOKIE_SECURE = False  # True for only https
