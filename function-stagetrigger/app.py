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
            loaded = dw.load_track(session, path_dict, media_json, ms)
            if loaded:
                ms.transformed = 1

        elif ms.path_type == 'album':
            media_json = spotify.get_album_info(ms.path)
            loaded = dw.load_album(session, path_dict, media_json, ms)
            if loaded:
                ms.transformed = 1

        elif ms.path_type == 'artist':
            media_json = spotify.get_artist_info(ms.path)
            loaded = dw.load_artist(session, path_dict, media_json)
            if loaded:
                ms.transformed = 1

        elif ms.path_type == 'playlist':
            media_json = spotify.get_playlist_info(ms.path)
            loaded = dw.load_playlist(session, path_dict, media_json, ms)
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
