import os
import re

WHITELIST_PATH = os.getenv('WHITELIST_PATH')


def parse_message(message, platform):
    url, text = parse_url(message)
    if not url:
        return

    if platform == 'spotify':
        try:
            url_string = url.split('/')
            path_id = url_string[-1].split('?')[0]
            path_type = url_string[-2]

            return path_id, path_type, "spotify", text
        except Exception as e:
            return None

    elif platform == 'youtube':
        url, text = parse_url(message)
        if not url:
            return

        try:
            url_string = url.split('/')[-1]
            path_id = url_string.split('=')[-1].split('?')[0]
            return path_id, "link", "youtube", text
        except Exception as e:
            return None

    elif platform == 'youtube_short':
        url, text = parse_url(message)
        if not url:
            return

        try:
            url_string = url.split('/')[-1]
            path_id = url_string.split('?')[0]
            return path_id, "link", "youtube", text
        except Exception as e:
            return None

    else:
        return None


def parse_url(message):
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
    if len(url) < 1:
        return None, None

    url = url[0]
    text = message.replace(url, '')
    return url, text.strip()


def not_in_whitelist(message):
    whitelist = []
    filename = os.path.join(
        os.path.dirname(__file__), '', 'whitelist.txt')

    with open(filename, 'r') as w_file:
        for chat_id in w_file:
            whitelist.append(chat_id.strip('\n'))

    try:
        chat_id = str(message['message']['chat']['id'])
        chat_title = str(message['message']['chat']['title'])
        if chat_id in whitelist:
            return False, chat_title
        else:
            return True, chat_title
    except:
        return True

