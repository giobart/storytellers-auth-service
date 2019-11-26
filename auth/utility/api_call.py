import requests
import auth
import logging
from flask import current_app as app
import json

'''
call the user service in order to validate the current userid and the password
if the call goes right from the openapi specification of the endpoint we have

response 200:
    return param: {"id":integer, "username": string, "password": stirng }
oterwise
    400 Bad Request
    401 Unauthorized

'''


def api_call_user_login(username, password):
    request_body = {"username": username, "password": password}

    logging.info("LOGIN WITH username:" + username)

    response = requests.post(app.config["USERS_ENDPOINT"] + auth.api_config['USERS_VALIDATE_USERNAME_URL'],
                             json=json.dumps(request_body))

    # If user correctly logged in then return user info otw raise exception
    if response.status_code == 200:
        json_response = response.json()

        return generate_identity(json_response)
    elif response.status_code == 401:
        raise InvalidUser("invalid username or password")
    else:
        raise ServerError("Server response not recognized")


def generate_identity(user):
    return {"username": user["username"], "password": user["password"], "id": user["id"]}


class InvalidUser(Exception):
    def __init__(self, value):
        self.value = value

class ServerError(Exception):
    def __init__(self, value):
        self.value = value
