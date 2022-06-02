import logging
import argparse

from lib import delete_messages, archive_messages, preview_messages


def parse_options():
    parser = argparse.ArgumentParser(description="Operate on Gmail messages matching a search expression")
    parser.add_argument('search_expr', type=str, help='message search expression', nargs='+')
    parser.add_argument('-n', '--max', type=int, help='limit max number of messages to process', default=10)
    parser.add_argument('-a', '--archive', help='archive matching messages to local disk', action='store_true')
    parser.add_argument('-d', '--delete', help='permanently delete matching messages', action='store_true')

    args = parser.parse_args()

    if hasattr(args,'help'):
        parser.print_help()
        exit(0)

    return args


if __name__ == "__main__":
    log = logging.getLogger()
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter('%(asctime)s\t -- %(message)s'))
    log.setLevel(logging.INFO)
    log.addHandler(console)

    opts = parse_options()

    log.info("Running operator... %s", opts)
    search_expr = ' '.join(opts.search_expr)

    if opts.delete:
        delete_messages(search_expr, opts.max)
    elif opts.archive:
        archive_messages(search_expr, opts.max)
    else:
        preview_messages(search_expr, opts.max)
