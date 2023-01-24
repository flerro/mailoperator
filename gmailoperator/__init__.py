from .gmail_api import gmail_client, search_messages, download_message, delete_message

__version__ = '0.1.0'

def download_messages(search_string, max_pages):
    service = gmail_client()
    search_messages(service, search_string,
                          action=download_message, max_messages=max_pages)


def delete_messages(search_string, max_pages):
    service = gmail_client()
    search_messages(service, search_string,
                          action=delete_message, max_messages=max_pages)


def preview_messages(search_string, max_pages):
    service = gmail_client()
    search_messages(service, search_string, max_messages=max_pages)