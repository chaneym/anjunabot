import os
import json
import boto3
from chalicelib import parsers
from chalice import Chalice

ENV_NAME = os.getenv('ENV_NAME')
SNS_TOPIC = os.getenv('SNS_TOPIC')

app = Chalice(app_name='anjunabot-{env}'.format(env=ENV_NAME))


@app.route('/', methods=['POST'])
def lambda_handler(event=None):
    if event:
        message = event
    else:
        try:
            message = app.current_request.json_body
        except Exception as e:
            print(e)
            return {'statusCode': 200}

    if parsers.not_in_whitelist(message):
        print('Bot in unknown room.')
        return {'statusCode': 200}

    path = None
    path_type = None
    platform = None
    text = None
    try:
        first_name = message['message']['from']['first_name']
        last_name = message['message']['from']['last_name'] if 'last_name' in message['message']['from'] else None
        chat_id = message['message']['chat']['id']
        chat_title = message['message']['chat']['title']
    except Exception as e:
        print(e)
        return {'statusCode': 200}

    try:
        if "spotify" in message['message']['text']:
            path, path_type, platform, text = parsers.parse_message(message['message']['text'], 'spotify')
        if "youtube" in message['message']['text']:
            path, path_type, platform, text = parsers.parse_message(message['message']['text'], 'youtube')
        if "youtu.be" in message['message']['text']:
            path, path_type, platform, text = parsers.parse_message(message['message']['text'], 'youtube_short')
    except Exception as e:
        print(e)
        return {'statusCode': 200}

    if path:
        topic_message = {
            "path": path,
            "path_type": path_type,
            "first_name": first_name,
            "last_name": last_name,
            "text": text,
            "chat_id": chat_id,
            "chat_title": chat_title,
            "platform": platform
        }
        try:
            if os.getenv('AWS_REGION') is not None:  # check if local test or lambda invocation
                sns = boto3.client('sns', region_name='us-west-2')
                response = sns.publish(TopicArn=SNS_TOPIC, Message=json.dumps(topic_message))
                return {'statusCode': 200}
            else:
                print(topic_message)

        except Exception as e:
            print(e)
            return {'statusCode': 200}

    else:
        # print('No Track ID Found.')
        return {'statusCode': 200}
