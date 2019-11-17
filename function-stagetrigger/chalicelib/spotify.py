import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')


def spotify_auth():
    client_credential_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credential_manager)

    return sp


def get_track_info(track_id):
    return spotify_auth().track(track_id)


def get_album_info(album_id):
    return spotify_auth().album(album_id)


def get_artist_info(artist_id):
    return spotify_auth().artist(artist_id)


def get_playlist_info(playlist_id):
    return spotify_auth().user_playlist(None, playlist_id)
