from datetime import datetime
import email


def extract_message_metadata(msg):
    payload = msg['payload']
    headers = payload.get("headers")
    h = {(h['name'].lower()):h['value'] for h in headers}
    try:
        h['date'] = email.utils.parsedate_to_datetime(h['date'])
    except ValueError:
        h['date'] = datetime(2000, 1, 1) # Placeholder date, GMail service launched on 2004
    h['size'] = size_format(msg['sizeEstimate'])
    return h


def message_info(headers):
    dt = headers['date'].strftime('%Y-%m-%d %H:%M:%S')
    return 'At: %s, Size: %s, From: %s, Subject: %s' % (dt, headers['size'], headers['from'], headers['subject'])


def size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"


def safe_file_name(text):
    return "".join(c if c.isalnum() else "_" for c in text).replace("__", "_")