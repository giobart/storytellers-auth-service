import json
import requests
import auth

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
    response = requests.post(auth.api_config['USERS_BASE_URL'] + auth.api_config['USERS_VALIDATE_USERNAME_URL'],
                             json=request_body)

    # If user correctly logged in then return user info otw raise exception
    if response.status_code == 200:
        json_response = json.loads(response.json())

        # Double check of username and password just to be sure that request was correctly validated
        if json_response["username"] == username and json_response["password"] == password:
            return generate_identity(json_response)
        else:
            raise InvalidUser("invalid username or password")
    else:
        raise InvalidUser("invalid username or password")


def generate_identity(user):
    return {"username": user["username"], "password": user["password"], "id": user["id"]}


class InvalidUser(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
