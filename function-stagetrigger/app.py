import os
import json
from chalicelib import spotify
from chalicelib import data_warehouse as dw
from chalice import Chalice

ENV_NAME = os.getenv('ENV_NAME')
app = Chalice(app_name='stagetrigger-{env}'.format(env=ENV_NAME))


@app.on_sns_message(topic='topic-dbstage-{env}'.format(env=ENV_NAME))
def lambda_handler(event):
        if os.getenv('AWS_REGION') is not None:
            row_id = json.loads(event.message)['row_id']
        else:
            row_id = event['row_id']

        session = dw.get_session()

        ms = dw.get_message_row_by_id(session, row_id)
        if ms.transformed == 1:
            return

        person_dict = {'first_name': ms.first_name, 'last_name': ms.last_name, 'user_id': ms.user_id}
        chat_dict = {'cid': ms.chat_id, 'title': ms.chat_title}
        path_dict = {'type': ms.path_type, 'uri': ms.path, 'platform': ms.platform}
        dw.load_post(session, chat_dict, person_dict, path_dict, ms.text)

        if ms.platform == 'spotify':

            if ms.path_type == 'track':
                media_json = spotify.get_track_info(ms.path)
                artist_dicts = get_artist_dict(session, media_json['artists'], ms.platform)
                album_path_dict = {'type': 'album', 'uri': media_json['album']['id'], 'platform': ms.platform}
                album_path = dw.load_path(session, album_path_dict)

                album_dict = {'path': album_path, 'title': media_json['album']['name'], 'type': media_json['album']['album_type'],
                              'num_tracks': media_json['album']['total_tracks']}

                track_dict = {'title': media_json['name']}
                loaded = dw.load_track(session, path_dict, track_dict, artist_dicts, [album_dict])
                if loaded:
                    ms.transformed = 1

            elif ms.path_type == 'album':
                media_json = spotify.get_album_info(ms.path)

                artist_dicts = get_artist_dict(session, media_json['artists'], ms.platform)

                track_dicts = get_track_dict(session, media_json['tracks']['items'], ms.platform, 'album')

                album_dict = {'title': media_json['name'], 'type': media_json['album_type'], 'num_tracks': media_json['total_tracks']}
                loaded = dw.load_album(session, album_dict, path_dict, artist_dicts, track_dicts)
                if loaded:
                    ms.transformed = 1

            elif ms.path_type == 'artist':
                media_json = spotify.get_artist_info(ms.path)

                genre_dicts = []
                for genre_name in media_json['genres']:
                    genre_dict = {'name': genre_name}
                    genre_dicts.append(genre_dict)

                artist_dict = {'name': media_json['name']}
                loaded = dw.load_artist(session, artist_dict, path_dict, genre_dicts)
                if loaded:
                    ms.transformed = 1

            if ms.path_type == 'playlist':
                media_json = spotify.get_playlist_info(ms.path)
                track_dicts = get_track_dict(session, media_json['tracks']['items'], ms.platform, 'playlist')
                playlist_dict = {'title': media_json['name']}
                loaded = dw.load_playlist(session, path_dict, playlist_dict, track_dicts)
                if loaded:
                    ms.transformed = 1

            else:
                # Unsupported path type
                pass

        try:
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
        finally:
            session.close()


def get_artist_dict(session, artist_json, platform):
    dicts = []
    for artist in artist_json:
        artist_path_dict = {'type': 'artist', 'uri': artist['id'], 'platform': platform}
        artist_path = dw.load_path(session, artist_path_dict)
        d = {'path': artist_path, 'name': artist['name']}
        dicts.append(d)
    return dicts


def get_track_dict(session, track_json, platform, track_type):
    dicts = []
    for track in track_json:
        if track_type == 'playlist':
            track = track['track']
        track_path_dict = {'type': 'track', 'uri': track['id'], 'platform': platform}
        track_path = dw.load_path(session, track_path_dict)
        t = {'path': track_path, 'title': track['name']}
        dicts.append(t)

    return dicts
