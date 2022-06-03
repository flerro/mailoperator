# gmail-operator

Perform operations on Gmail messages matching a [search expression](https://support.google.com/mail/answer/7190?hl=en).

## Usage

```bash
usage: operator.py [-h] [-n MAX_MESSAGES] [--archive] [--delete] search_expr

Perform operations on Gmail messages matching a search expression

positional arguments:
  search_expr           message search expression

options:
  -h, --help            show this help message and exit
  -n MAX_MESSAGES, --max-messages MAX_MESSAGES
                        limit max number of messages to process
  --archive             archive matching messages to local disk
  --delete              permanently delete matching messages
```

Examples:

- List latest 10 messages containing the 'unsubscribe' keyword
    ```
    $ python operator.py 'unsubscribe older:2022/05/10'
    ```

- Delete latest 10 messages received from the given sender
    ```
    $ python operator.py --delete 'from:test@test.com'
    ```

- Delete latest 100 messages categorized in the "Promotions" tab
    ```
    $ python operator.py --delete 'label:promotions' -n 100
    ```

- Save locally latest 200 messages matching the given search expression (message containing 'unsubscribe' keyword but not 'jugmilano' and received before '2022-05-10')
    ```
    $ python operator.py --archive 'unsubscribe -jugmilano older:2022/05/10' -n 200
    ```

Standard [GMail search expression](https://support.google.com/mail/answer/7190?hl=en) syntax is supported.

## Get API credentials

To use the Gmail API, we need an auth token: 

1. Go to the [GCP Project Dashboard](https://console.developers.google.com/apis/dashboard)
2. Click on `Enable API button` and search for `GMail API`
3. Select`Credential` section on the left panel, click con `Create Credentials > OAuth Client ID`
4. Rename the downloaded JSON as `credentials.json` and move it to the `gmail-operator` directory 

More [info here](https://developers.google.com/workspace/guides/create-credentials)

## Links

- API reference: https://developers.google.com/gmail/api
- Search syntax: https://support.google.com/mail/answer/7190?hl=en
