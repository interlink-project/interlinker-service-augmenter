from flask import Blueprint
import requests

from flask import Flask, render_template, redirect, request, url_for, session
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from authInterlink.helpers import  config
from authInterlink.user import User

authInterlink = Blueprint('authInterlink', __name__,template_folder="./website/templates")

APP_STATE = 'ApplicationState'
NONCE = 'SampleNonce'

@authInterlink.route("/login")
def login():
    # get request params
    query_params = {'client_id': config["client_id"],
                    'redirect_uri': config["redirect_uri"],
                    'scope': "openid email profile",
                    'state': APP_STATE,
                    'nonce': NONCE,
                    'response_type': 'code',
                    'response_mode': 'query'}

    # build request_uri
    request_uri = "{base_url}?{query_params}".format(
        base_url=config["auth_uri"],
        query_params=requests.compat.urlencode(query_params)
    )

    return redirect(request_uri)



@authInterlink.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


@authInterlink.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@authInterlink.route("/oidc_callback")
def callback():
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    code = request.args.get("code")
    if not code:
        return "The code was not returned or is not accessible", 403
    query_params = {'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': request.base_url
                    }
    query_params = requests.compat.urlencode(query_params)
    exchange = requests.post(
        config["token_uri"],
        headers=headers,
        data=query_params,
        auth=(config["client_id"], config["client_secret"]),
    ).json()

    # Get tokens and validate
    if not exchange.get("token_type"):
        return "Unsupported token type. Should be 'Bearer'.", 403
    access_token = exchange["access_token"]
    id_token = exchange["id_token"]

    session['id_token']=id_token

    #if not is_access_token_valid(access_token, config["issuer"], config["client_id"]):
    #    return "Access token is invalid", 403

    #if not is_id_token_valid(id_token, config["issuer"], config["client_id"], NONCE):
    #    return "ID token is invalid", 403

    # Authorization flow successful, get userinfo and login user
    userinfo_response = requests.get(config["userinfo_uri"],
                                     headers={'Authorization': f'Bearer {access_token}'}).json()

    unique_id = userinfo_response["sub"]
    user_email = userinfo_response["email"]
    user_name = userinfo_response["given_name"]

    user = User(
        id_=unique_id, name=user_name, email=user_email
    )

    if not User.get(unique_id):
        User.create(unique_id, user_name, user_email)

    login_user(user)
   # g.user =user

    return redirect(url_for("authInterlink.dashboard"))


@authInterlink.route("/logout", methods=["GET", "POST"])
@login_required
def logout():

    logout_user()
    
    
    #response = redirect(config["end_session_endpoint"])

    payload = {'id_token_hint': session['id_token'],
                    'post_logout_redirect_uri': "http://127.0.0.1:5000/home",
                    'state': APP_STATE}

    #headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    r = requests.get(
        config["end_session_endpoint"],
        params=payload,
    )

    r.url

    r.text

    


    #return response
    #return render_template("home.html")
    return redirect(config["end_session_endpoint"]) #Por ahora queda asi.