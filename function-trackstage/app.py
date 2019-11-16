import os
import json
from chalicelib import dbops, spotify
from chalice import Chalice

ENV_NAME = os.getenv('ENV_NAME')
app = Chalice(app_name='trackstage-{env}'.format(env=ENV_NAME))


@app.on_sns_message(topic='anjunabot-sendtrack-{env}'.format(env=ENV_NAME))
def lambda_handler(event):
    topic_message = json.loads(event.message)

    person = topic_message['person']
    path = topic_message['path']
    path_type = topic_message['path_type']
    platform = topic_message['platform']
    comment = topic_message['comment']
    chat_id = topic_message['chat_id']
    chat_title = topic_message['chat_title']

    # stage the message for transformation into dim/fact tables
    dbops.message_stage(path=path, path_type=path_type, platform=platform, person=person, comment=comment,
                        chat_id=chat_id, chat_title=chat_title)

    # if it's a spotify track insert it into the playlist
    if platform == 'spotify' and path_type == 'track':
        spotify.add_track_to_playlist(path)

    return {'statusCode': 200}
