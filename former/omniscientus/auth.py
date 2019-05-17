import functools
import json

from flask import Blueprint, g, redirect, request, session, url_for, jsonify
from google.oauth2.credentials import Credentials
from google_auth_oauthlib import flow as _flow
from googleapiclient import discovery
from omniscientus import api_methods as apmt
from omniscientus.utils.google.goauth import API_SERVICE_NAME, API_VERSION, CLIENT_SECRETS_FILE, \
    channels_list_by_username, REDIRECT_URI, SCOPES

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login')
def login():
    if 'credentials' not in session:
        return redirect(url_for('auth.authorize'))

    # Load the credentials from the session.
    credentials = Credentials(**session['credentials'])

    client = discovery.build(API_SERVICE_NAME, API_VERSION, credentials=credentials, cache_discovery=False)

    # response şekli değiştirilecek
    # yt_client.channels().list(part='snippet,contentDetails,statistics,topicDetails',
    # id="UCrVR30q-Seo82gBhmAe_1uQ").execute()
    channel_info_response = channels_list_by_username(client,
                                                      part='snippet,contentDetails,statistics,topicDetails',
                                                      mine=True)

    apmt.channel_add(channel_info_response["items"][0]["id"])

    session['channel_info'] = channel_info_response

    return jsonify(apmt.channel_get_one(channel_info_response["items"][0]["id"]))


@bp.route('/authorize')
def authorize():
    # Create a flow instance to manage the OAuth 2.0 Authorization Grant Flow
    # steps.
    print("1")
    flow = _flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
    print("2")
    flow.redirect_uri = url_for('auth.' + REDIRECT_URI, _external=True)
    print(flow.redirect_uri)
    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='false')
    print("3")
    # Store the state in the session so that the callback can verify that
    # the authorization server response.
    session['state'] = state
    print(authorization_url)
    return redirect(authorization_url)


@bp.route(REDIRECT_URI)
def oauth2callback():
    print("x")
    # Specify the state when creating the flow in the callback so that it can
    # verify the authorization server response.
    state = session['state']
    print("2")
    flow = _flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    print(flow.redirect_uri)
    flow.redirect_uri = url_for('auth.' + REDIRECT_URI, _external=True)
    print("1")
    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    # Store the credentials in the session.
    # ACTION ITEM for developers:
    #     Store user's access and refresh tokens in your data store if
    #     incorporating this code into your real app.
    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

    return redirect(url_for('auth.login'))


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        print(view)
        if 'credentials' not in session:
            return redirect(url_for('auth.authorize'))
        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    channel_credentials = session.get('credentials')

    if channel_credentials is None:
        g.user = None
    else:
        g.user = channel_credentials
