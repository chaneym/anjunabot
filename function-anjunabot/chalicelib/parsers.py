import re


def parse_spotify(message):
    url, comment = parse_url(message)
    if not url:
        return

    try:
        url_string = url.split('/')
        track_id = url_string[-1].split('?')[0]
        return track_id, comment, "spotify"
    except Exception as e:
        return None


def parse_youtube(message):
    url, comment = parse_url(message)
    if not url:
        return

    try:
        url_string = url.split('/')
        track_id = url_string[-1].split('=')[-1]
        return track_id, comment,  "youtube"
    except Exception as e:
        return None


def parse_youtube_short(message):
    url, comment = parse_url(message)
    if not url:
        return

    try:
        track_id = url.split('/')
        return track_id, comment, "youtube"
    except Exception as e:
        return None


def parse_url(message):
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
    if len(url) < 1:
        return None, None

    url = url[0]
    comment = message.replace(url, '')
    return url, comment.strip()
