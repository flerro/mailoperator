import base64
import os
import pickle
import logging

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import formatters as fmt

SCOPES = ['https://mail.google.com/']
CLIENT_SECRET = 'client_secret.json'

log = logging.getLogger()


def gmail_client(account_name='default'):
    """
    Generate a new GMail API client, handling authorization. 
    
    The '<account_name>.pickle' file stores the user's access and refresh tokens.
    Auth credentials are loaded from <account_name>.pickle if the file is present
    Otherwise, if there are no (valid) credentials available, the log in 
    flow is triggered.

    The '<account_name>.pickle' file is created automatically when the authorization
    flow completes for the first time.
    
    """
    creds = None
    token_pickle = account_name + '_secret.pickle'
    if os.path.exists(token_pickle):
        with open(token_pickle, "rb") as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_pickle, "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)


def preview_metadata(gmail, message, options):
    """
    Log in output GMail message metadata, including: 
    subject, sender, received date, size, labels.

    Args:
        gmail: a GMail API client
        :param options: needed for method signature compatibility, but not used
    """
    msg = gmail.users().messages().get(userId='me', id=message['id'], format='metadata').execute()    
    # print(fmt.message_info_metadata(msg), msg['labelIds'])
    print(fmt.message_info_metadata(msg))


def delete_message(gmail, message, options=None):
    """Permanetly deletes a GMail message

    Args:
        gmail: a GMail API client
        message: a GMail message
        :param options: needed for method signature compatibility, but not used
    """
    msg = gmail.users().messages().get(userId='me', id=message['id'], format='metadata').execute()
    headers = fmt.extract_message_metadata(msg)
    print(fmt.message_info(headers))
    gmail.users().messages().delete(userId='me', id=message['id']).execute()


def search_messages(gmail, search_expr, action=preview_metadata, max_messages=10, options=None):
    """
    Search for GMail messages mathing the given search expression, then perform 
    an operation on each message. Default operation is `preview_metadata`.

    Args:
        gmail: a GMail API client
        search_expr: search expression
        action: operation to execute on each matching message
        max_messages: max messages to process 
        :param options: additional parameters for downstream operations
    """
    msg_count = 0
    result = gmail.users().messages().list(userId='me', q=search_expr).execute()

    if 'messages' in result:
        print(fmt.message_info_title())
        for message in result['messages']:
            if msg_count >= max_messages:
                return
            action(gmail, message, options)
            msg_count += 1

    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = gmail.users().messages().list(userId='me', q=search_expr, pageToken=page_token).execute()
        if 'messages' in result and msg_count < max_messages:
            for message in result['messages']:
                if msg_count >= max_messages:
                    return
                action(gmail, message, options)
                msg_count += 1


def download_message(gmail, message, options):
    """Store GMail message as an eml file
    
    Args:
        gmail: a GMail API client
        message: a GMail message
        options: should include information about account
    """
    msg_with_headers = gmail.users().messages().get(userId='me', id=message['id'], format='metadata').execute()
    headers = fmt.extract_message_metadata(msg_with_headers)
    print(fmt.message_info(headers))

    msg = gmail.users().messages().get(userId='me', id=message['id'], format='raw').execute()
    raw = msg['raw']

    prefix = options['account'] if 'account' in options else 'default'
    base_path = '%s_account' % prefix
    recv_date = headers['date'].strftime('%Y-%m-%d').replace('-', os.path.sep)
    path = os.path.join(base_path, msg['labelIds'][-1], recv_date)

    if not os.path.isdir(path):
        os.makedirs(path)
    out_file = os.path.join(path, '%s.eml' % fmt.safe_file_name(headers['subject']))
    with open(out_file, 'wb') as f:
        f.write(base64.urlsafe_b64decode(raw + "========"))

