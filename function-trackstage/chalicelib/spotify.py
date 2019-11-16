import os
import json
import requests

USER_NAME = os.environ['USER_NAME']
PASSWORD = os.environ['PASSWORD']
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']
PLAYLIST_ID = os.environ['PLAYLIST_ID']
USER_ID = os.environ['USER_ID']
SCOPE = os.environ['SCOPE']
CALLBACK = os.environ['CALLBACK']
AUTH_TOKEN = os.environ['AUTH_TOKEN']
REFRESH_TOKEN = os.environ['REFRESH_TOKEN']


def add_track_to_playlist(track_id):
    if track_in_is_playlist(track_id):
        return

    url = 'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?'.format(playlist_id=PLAYLIST_ID)
    req_headers = get_headers()
    if not req_headers:
        return

    req_body = {"uris": ["spotify:track:{track_id}".format(track_id=track_id)]}
    r = requests.post(url, headers=req_headers, data=json.dumps(req_body))

    try:
        r.raise_for_status()
    except:
        return


def get_tracks_in_playlist():
    url = 'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?'.format(playlist_id=PLAYLIST_ID)
    req_headers = get_headers()
    if not req_headers:
        return

    r = requests.get(url, headers=req_headers)

    try:
        r.raise_for_status()
        return r.json()
    except:
        return


def track_in_is_playlist(track_id):
    playlist = get_tracks_in_playlist()
    for item in playlist['items']:
        if item['track']['id'] == track_id:
            return True
    return False


def get_headers():
    token = get_access_token()
    if not token:
        return None

    return {"Authorization": "Bearer {0}".format(token), 'Content-Type': 'application/json'}


def get_access_token():
    req_header = {'Authorization': 'Basic {}'.format(AUTH_TOKEN)}
    req_body = {'grant_type': 'refresh_token', 'refresh_token': REFRESH_TOKEN}
    r = requests.post('https://accounts.spotify.com/api/token', headers=req_header, data=req_body)
    res_json = r.json()

    try:
        access_token = res_json['access_token']
        return access_token
    except:
        return None