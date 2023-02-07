import argparse
import logging
import sys

import operations as op


def parse_options():
    parser = argparse.ArgumentParser(description="Perform operations on Gmail messages matching a search expression")
    parser.add_argument('search_expr', type=str, help='Gmail search expression')
    parser.add_argument('-u', '--account', type=str,
                        help='use non default authentication file', default='token.pickle')
    parser.add_argument('-n', '--max-messages', type=int,
                        help='max number of messages to process (default: 10)', default=10)
    parser.add_argument('--dload', help='download matching messages', action='store_true')
    parser.add_argument('--remove', help='permanently delete matching messages', action='store_true')

    args = parser.parse_args()

    if hasattr(args, 'help'):
        parser.print_help()
        exit(0)

    return args


def run():
    try:
        logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)

        opts = parse_options()

        print("Running operator...", str(opts)[10:-1])
        search_expr = opts.search_expr

        if opts.dload:
            op.download_messages(search_expr, opts.max_messages, opts.account)
        elif opts.remove:
            op.delete_messages(search_expr, opts.max_messages, opts.account)
        else:
            op.preview_messages(search_expr, opts.max_messages, opts.account)
    except KeyboardInterrupt:
        print("Bye!")
    except Exception as e:
        print("Sorry, something did not work as expected...", str(e), file=sys.stderr)


