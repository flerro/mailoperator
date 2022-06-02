import base64
import os
import pickle
import logging

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from gmail_api_utils import extract_message_metadata, message_info, clean


SCOPES = ['https://mail.google.com/']

log = logging.getLogger()


def gmail_client():
    """
    Generate a new GMail API client, handling authorization. 
    
    The 'token.pickle' file stores the user's access and refresh tokens.
    Auth credentials are loaded from token.pickle if the file is present
    Otherwise, if there are no (valid) credentials available, the log in 
    flow is triggered.

    The 'token.pickle' file is created automatically when the authorization 
    flow completes for the first time.
    
    """
    creds = None
    token_pickle = "token.pickle"

    if os.path.exists(token_pickle):
        with open(token_pickle, "rb") as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_pickle, "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)


def preview_metadata(gmail, message):
    msg = gmail.users().messages().get(userId='me', id=message['id'], format='metadata').execute()
    headers = extract_message_metadata(msg)
    log.info("Match... %s", message_info(headers))


def delete_message(gmail, message):
    """Permanetly deletes a GMail message

    Args:
        gmail: a GMail API client
        message: a GMail message
    """
    msg = gmail.users().messages().get(userId='me', id=message['id'], format='metadata').execute()
    headers = extract_message_metadata(msg)
    log.info("Deleting... %s", message_info(headers))
    gmail.users().messages().delete(userId='me', id=message['id']).execute()


def search_messages(gmail, search_expr, action=preview_metadata, max_messages=10):
    """
    Search for GMail messages mathing the given search expression, then perform 
    an operation on eacn message. Default operation is `preview_metadata`.

    Args:
        gmail: a GMail API client
        search_expr: search expression
        action: operation to execute on each matching message
        max_messages: max messages to process 
    """
    msg_count = 0
    result = gmail.users().messages().list(userId='me',q=search_expr).execute()

    if 'messages' in result:
        for message in result['messages']:
            if msg_count >= max_messages: return
            action(gmail, message)
            msg_count += 1

    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = gmail.users().messages().list(userId='me',q=search_expr, pageToken=page_token).execute()
        if 'messages' in result and msg_count < max_messages:
            for message in result['messages']:
                if msg_count >= max_messages: return
                action(gmail, message)
                msg_count += 1


def dump_message(gmail, message, base_path='account'):
    """Store GMail message as an eml file
    
    Args:
        gmail: a GMail API client
        message: a GMail message
        base_path (str, optional): base ouput path relative to current directory. Defaults to 'account'.
    """
    msg = gmail.users().messages().get(userId='me', id=message['id'], format='metadata').execute()
    headers = extract_message_metadata(msg)

    log.info("Archiving... %s", message_info(headers))

    msg = gmail.users().messages().get(userId='me', id=message['id'], format='raw').execute()
    raw = msg['raw']

    recv_date = headers['date'].strftime('%Y-%m-%d').replace('-', os.path.sep)
    path = os.path.join(base_path, 'inbox', recv_date)
    if not os.path.isdir(path):
        os.makedirs(path)
    out_file = os.path.join(path, '%s.eml' % clean(headers['subject']))
    with open(out_file, 'wb') as f:
        f.write(base64.urlsafe_b64decode(raw + "========"))

