import gmail_api as api


def download_messages(search_string, max_pages, account):
    service = api.gmail_client(account_name=account)
    api.search_messages(service, search_string,
                        action=api.download_message, max_messages=max_pages,
                        options={'account': account})


def delete_messages(search_string, max_pages, account):
    service = api.gmail_client(account_name=account)
    api.search_messages(service, search_string,
                        action=api.delete_message, max_messages=max_pages)


def preview_messages(search_string, max_pages, account):
    service = api.gmail_client(account_name=account)
    api.search_messages(service, search_string, max_messages=max_pages)
