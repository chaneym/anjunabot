import os
import json
from app import lambda_handler


def test_lambda_handler():
    chat_events = load_chat_events()
    for event in chat_events:
        print('Sending Chat Event: {}'.format(event['event_type']))
        lambda_handler(event)


def load_chat_events():
    path = 'chat_event/'
    chat_events = []
    for filename in os.listdir(path):
        with open(os.path.join(path, filename)) as test_file:
            chat_events.append(json.load(test_file))

    return chat_events


if __name__ == '__main__':
    test_lambda_handler()
