# mail-operator

**mail-operator** is a CLI utility to manage your Gmail inbox. Currently supported operations include listing, removing and downloading messages. Target messages are selecte via a [search expression](https://support.google.com/mail/answer/7190?hl=en). 

**mail-operator** is very [privacy friendly](https://github.com/flerro/mailoperator/blob/master/PRIVACY_POLICY.md), the code is publicly available on [Github](https://github.com/flerro/mailoperator).

## Install

1. Download package locally

      ```
      git clone https://github.com/flerro/mailoperator
      ```

2. Install globally using `pip`

      ```
   cd mailoperator 
   pip3 install .
      ```
   
BTW Global installation is not mandatory, you can use the tool from a [virtualenv](https://realpython.com/python-virtual-environments-a-primer/) ;)

## Usage

```bash
usage: mop [-h] [-u ACCOUNT] [-n MAX_MESSAGES] [--cp] [--rm] search_expr

Perform operations on Gmail messages matching a search expression

positional arguments:
  search_expr           message search expression

options:
  -h, --help            show this help message and exit
  -u ACCOUNT, --account ACCOUNT
                        use non default credentials file
  -n MAX_MESSAGES, --max-messages MAX_MESSAGES
                        max number of messages to process (default: 10)
  --cp                  download matching messages
  --rm                  permanently delete matching messages
```

The standard [GMail search expression](https://support.google.com/mail/answer/7190?hl=en) syntax is supported for `search_expr`.

Operations are executed on messages in reverse temporal order (latest messages first), 10 messages are processed by default.

### Usage examples


- List 10 messages containing the 'unsubscribe' keyword, received after 2022-05-10
    ```
    mop 'unsubscribe older:2022/05/10'
    ```

- List messages containing the 'unsubscribe' keyword, using authentication stored in 'francesco.pickle'
    ```
    mop 'unsubscribe' -u francesco
    ```
  
- Delete 10 messages received from the given sender
    ```
    mop --rm 'from:test@test.com' 
    ```

- Delete 100 messages categorized in the "Promotions" tab
    ```
    mop --rm 'label:promotions' -n 100
    ```

- Download 200 messages matching the given search expression (message containing 'unsubscribe' keyword but not 'jugmilano' and received before '2022-05-10')
    ```
    mop --cp 'unsubscribe -jugmilano older:2022/05/10' -n 200
    ```
  
Please note that the `mop` command is available only if the package is installed globally, otherwise use `./operator.py` script to start **mail-operator**.

## Get Google API client secret

To use the Gmail API, we need allow oauth authentication: 

1. Go to the [GCP Project Dashboard](https://console.developers.google.com/apis/dashboard)
2. Click on `Enable API button` and search for `GMail API`
3. Select`Credential` section on the left panel, click con `Create Credentials > OAuth Client ID`
4. Rename the downloaded JSON as `client_secret.json` and move it to the `mailoperator` directory 

More [info here](https://developers.google.com/workspace/guides/create-credentials)

## Links

- API reference: https://developers.google.com/gmail/api
- Search syntax: https://support.google.com/mail/answer/7190?hl=en
- [Privacy policy](https://github.com/flerro/gmail-operator/blob/master/privacy_policy.md)
