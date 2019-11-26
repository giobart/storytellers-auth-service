import json


class TestAuth:

    # test correct user login
    def test_1_login(self, client, mock_login_user):
        # Mock status code of response.
        mock_login_user.return_value.status_code = 200
        mock_login_user.return_value.json.return_value = {"id": 2, "username": "test1", "password": "test1123"}

        loginreq = {
            "username": "test1",
            "password": "test1123",
        }

        reply = client.post('/auth/login', json=loginreq)
        assert reply.status_code == 200

        token_cookie = reply.headers.getlist('Set-Cookie')
        assert token_cookie is not None

    # test unexpected username server response
    def test_2_login(self, client, mock_login_user):
        # Mock status code of response.
        mock_login_user.return_value.status_code = 500
        mock_login_user.return_value.json.return_value = '{"id": 2, mmmm: 3333, "password": "test1123"}'

        loginreq = {
            "username": "test1",
            "password": "test1123",
        }

        reply = client.post('/auth/login', json=loginreq)
        assert reply.status_code == 401

        token_cookie = reply.headers.getlist('Set-Cookie')
        assert token_cookie == []

    # test strange server response
    def test_3_login(self, client, mock_login_user):
        # Mock status code of response.
        mock_login_user.return_value.status_code = 401
        mock_login_user.return_value.json.return_value = {"we": 2, "maronn": "coseAcaso", "belle": "pizza"}

        loginreq = {
            "username": "test1",
            "password": "test1123",
        }

        reply = client.post('/auth/login', json=loginreq)
        assert reply.status_code == 403

        token_cookie = reply.headers.getlist('Set-Cookie')
        assert token_cookie == []

        mock_login_user.return_value.status_code = 405
        reply = client.post('/auth/login', json=loginreq)
        assert reply.status_code == 401

    # test the logout
    def test_4_logout(self, client, mock_login_user):
        # Mock status code of response.
        mock_login_user.return_value.status_code = 200
        mock_login_user.return_value.json.return_value = {"id": 2, "username": "test1", "password": "test1123"}

        loginreq = {
            "username": "test1",
            "password": "test1123",
        }

        # login
        reply = client.post('/auth/login', json=loginreq)
        token_cookie = reply.headers.getlist('Set-Cookie')

        # perform logout
        reply = client.post('/auth/logout')
        assert reply.status_code == 200

        # check that the response set the expire token
        token_cookie = reply.headers.getlist('Set-Cookie')
        assert "Expires" in token_cookie[0]

        # perform logout again without token
        reply = client.post('/auth/logout')
        assert reply.status_code == 401

    # test the refresh token functionality
    def test_5_refresh(self, client, mock_login_user):
        # Mock status code of response.
        mock_login_user.return_value.status_code = 200
        mock_login_user.return_value.json.return_value = {"id": 2, "username": "test1", "password": "test1123"}

        loginreq = {
            "username": "test1",
            "password": "test1123",
        }

        # perform bad token refresh request using no token
        reply = client.post('/auth/token_refresh')
        assert reply.status_code == 401

        # login
        reply = client.post('/auth/login', json=loginreq)
        token_cookie = reply.headers.getlist('Set-Cookie')

        token_cookie = reply.headers.getlist('Set-Cookie')
        old_access_token = token_cookie[0]

        # perform correct token refresh request
        reply = client.post('/auth/token_refresh')
        assert reply.status_code == 200

        # check that the response set the new access token
        token_cookie = reply.headers.getlist('Set-Cookie')
        assert "access" in token_cookie[0]

        # check that new token is different than the old one
        assert token_cookie[0] != old_access_token

        # the logout should be performed normally
        reply = client.post('/auth/logout')
        assert reply.status_code == 200
