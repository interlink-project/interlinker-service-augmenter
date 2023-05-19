import jwt
from flask import request
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from jwt import PyJWKClient
import os

url = "https://aac.platform.smartcommunitylab.it/jwk"
jwks_client = PyJWKClient(url)


def decode_token(jwtoken):
    signing_key = jwks_client.get_signing_key_from_jwt(jwtoken)
    data = jwt.decode(
        jwtoken,
        signing_key.key,
        algorithms=["RS256"],
        audience=os.getenv("CLIENT_ID"),
        # options={"verify_exp": False},
    )
    return data


def get_token_in_cookie(request):
    try:
        return request.cookies.get("auth_token")
    except:
        return None


def get_token_in_header(request):
    try:
        return request.headers.get('authorization').replace("Bearer ", "")
    except:
        return None


def get_current_token(request):
    state = request.state._state
    return state["token"]


def get_current_user(request):
    try:
        token = get_token_in_cookie(request) or get_token_in_header(request)
        # gets user_data from state (see AuthMiddleware)
        if token:
            user_data = decode_token(token)
            return user_data
        return None
    except Exception as e:
       # print(str(e))
        return None


def get_current_active_user(current_user):
    # calls get_current_user, and if nothing is returned, raises Not authenticated exception

    if not current_user:
        return "Not authenticated", 403

    return current_user
