# gmail-operator

Perform operations on Gmail messages matching a [search expression](https://support.google.com/mail/answer/7190?hl=en).

## Usage

```bash
usage: operator.py [-h] [-m MAX] [-a] [-d] search_expr [search_expr ...]

Email Sender using Gmail API

positional arguments:
  search_expr        The expression to match search

options:
  -h, --help         show this help message and exit
  -m MAX, --max MAX  "pages" of messages to process
  -a, --archive      archive messages to disk
  -d, --delete       delete messages
```

Examples:

- List all message containing the 'unsubscribe' keyword, received before the given date
    ```
    $ python app/operator.py 'unsubscribe' 'older:2022/05/10'
    ```

- Delete all message received from the given sender
    ```
    $ python app/operator.py -d 'from:test@test.com'
    ```

- Save locally all message containing the 'unsubscribe' keyword and received before the given date
    ```
    $ python app/operator.py -d 'unsubscribe' 'older:2022/05/10'
    ```

Standard [GMail search expression](https://support.google.com/mail/answer/7190?hl=en) syntax is supported.

## Get an auth token 

To use the Gmail API, we need an auth token: 

1. Go to the [GCP Project Dashboard](https://console.developers.google.com/apis/dashboard)
2. Click on `Enable API button` and search for `GMail API`
3. Select`Credential` section on the left panel, click con `Create Credentials > OAuth Client ID`
4. Rename the downloaded JSON as `credentials.json` and move it to the `gmail-operator` directory 

## Links

- API reference: https://developers.google.com/gmail/api
- Search syntax: https://support.google.com/mail/answer/7190?hl=en
