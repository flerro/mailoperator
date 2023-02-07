from datetime import datetime
import email

MESSAGE_INFO_FMT = '%-16s | %8s | %-50s | %s'


def extract_message_metadata(msg):
    payload = msg['payload']
    headers = payload.get("headers")
    h = {(h['name'].lower()):h['value'] for h in headers}
    try:
        h['date'] = email.utils.parsedate_to_datetime(h['date'])
    except ValueError:
        # use Gmail service launch date as placeholder
        h['date'] = datetime(2004, 4, 1)
    h['size'] = size_format(msg['sizeEstimate'])
    return h


def message_info(headers):
    dt = headers['date'].strftime('%Y-%m-%d %H:%M')
    return MESSAGE_INFO_FMT % (dt, headers['size'], headers['subject'][:50], headers['from'])


def message_info_metadata(msg):
    headers = extract_message_metadata(msg)
    return message_info(headers)


def message_info_title():
    return MESSAGE_INFO_FMT % ('DATE', 'SIZE', 'SUBJECT', 'FROM')


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