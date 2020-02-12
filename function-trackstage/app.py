import os
import boto3
import json
from chalicelib import dbops, spotify
from chalice import Chalice

ENV_NAME = os.getenv('ENV_NAME')
SNS_TOPIC = os.getenv('SNS_TOPIC')

app = Chalice(app_name='trackstage-{env}'.format(env=ENV_NAME))


@app.on_sns_message(topic='topic-sendtrack-{env}'.format(env=ENV_NAME))
def lambda_handler(event):
    topic_message = json.loads(event.message)

    path = topic_message['path']
    path_type = topic_message['path_type']
    platform = topic_message['platform']

    # stage the message for transformation into dim/fact tables
    row_id = dbops.message_stage(topic_message)

    # if it's a spotify track insert it into the playlist
    if platform == 'spotify' and path_type == 'track':
        spotify.add_track_to_playlist(path)

    # notify ETL handler of new row
    if os.getenv('AWS_REGION') is not None:  # check if local test or lambda invocation
        sns = boto3.client('sns', region_name='us-west-2')
        sns.publish(TopicArn=SNS_TOPIC, Message=json.dumps({"row_id": row_id}))
    else:
        print(topic_message)

