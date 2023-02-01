#!/usr/bin/env python3

import argparse
import logging

import operations as op


def parse_options():
    parser = argparse.ArgumentParser(description="Perform operations on Gmail messages matching a search expression")
    parser.add_argument('search_expr', type=str, help='message search expression')
    parser.add_argument('-n', '--max-messages', type=int,
                        help='max number messages to return as search results', default=10)
    parser.add_argument('--cp', help='download matching messages', action='store_true')
    parser.add_argument('--rm', help='permanently delete matching messages', action='store_true')

    args = parser.parse_args()

    if hasattr(args, 'help'):
        parser.print_help()
        exit(0)

    return args


def run():
    try:
        log = logging.getLogger()
        console = logging.StreamHandler()
        console.setFormatter(logging.Formatter('%(asctime)s\t -- %(message)s'))
        log.setLevel(logging.INFO)
        log.addHandler(console)

        opts = parse_options()

        log.info("Running operator... %s", opts)
        search_expr = opts.search_expr

        if opts.cp:
            op.download_messages(search_expr, opts.max_messages)
        elif opts.rm:
            op.delete_messages(search_expr, opts.max_messages)
        else:
            op.preview_messages(search_expr, opts.max_messages)
    except KeyboardInterrupt:
        log.warning("Bye!")
    except Exception as e:
        log.warning("Sorry, something did not work as expected... ", str(e))


if __name__ == "__main__":
    run()

