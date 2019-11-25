from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required,
                                get_jwt_identity, get_raw_jwt, set_access_cookies,
                                set_refresh_cookies, unset_jwt_cookies)
from auth.utility.api_call import *

auth = Blueprint('auth', __name__)


''' 
    /login for the user, set refresh token and access token
    Tokens are composed of an identity object
    created as following:
        {"id":integer, "username":String, "password":String}
'''


@auth.route('/auth/login', methods=['POST'])
def login():
    req = request.json

    try:

        # getting username and password from input json
        username = req['username'].strip()
        password = req['password'].strip()

        # user validation
        user = api_call_user_login(username, password)

        # generation of the identity object from user_id, password and username
        identity = generate_identity(user)

        # access token and refresh token  generation
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)

        resp = jsonify({
            'id': identity["id"]
        })

        # settin cookie to the browser for access token and refresh token
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)

        return resp, 200

    except InvalidUser as e:
        return {'err': 'Wrong credentials'}, 401
    except Exception as e:
        return {'err': 'Something bad during auth'}, 401


''' /logout Reset the browser cache, the current login token will expire in 15 min and the refresh token in 30 days'''


@auth.route('/auth/logout', methods=['POST'])
@jwt_required
def logout():

    # check user identity from the access token
    identity = get_jwt_identity()

    if identity:
        resp = jsonify({
            'message': 'Logged out {}'.format(identity['username']),
        })

        # force che browser to unset the cookie for the current token
        unset_jwt_cookies(resp)

        return resp, 200
    else:
        abort(401)


''' /token_refresh Refresh the current expired login token '''


@auth.route('/auth/token_refresh', methods=['POST'])
@jwt_refresh_token_required
def token_refresh():

    # check user identity from the access token
    current_user = get_jwt_identity()

    # create a ne access token from the actual refresh token
    access_token = create_access_token(identity=current_user)

    resp = jsonify({'refresh': True})

    # set the browser cookie to the new refreshed access token
    set_access_cookies(resp, access_token)

    return resp, 200
