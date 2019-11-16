import re


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


