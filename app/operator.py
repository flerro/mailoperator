import logging
import gmail_api as gmail


def archive_messages(search_string, max_pages):
    service = gmail.auth()
    gmail.search_messages(service, search_string,
                          action=gmail.dump_message, max_pages=max_pages)


def delete_messages(search_string, max_pages):
    service = gmail.auth()
    gmail.search_messages(service, search_string,
                          action=gmail.delete_message, max_pages=max_pages)


def preview_messages(search_string, max_pages):
    service = gmail.auth()
    gmail.search_messages(service, search_string, max_pages=max_pages)


if __name__ == "__main__":

    logging.basicConfig(filename='operator.log',
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d,%H:%M:%S',
                        level=logging.INFO)

    import argparse
    parser = argparse.ArgumentParser(description="Email Sender using Gmail API")
    parser.add_argument('search_expr', type=str, help='The expression to match search', nargs='+')
    parser.add_argument('-m', '--max', type=int, help='"pages" of messages to process', default=1)
    parser.add_argument('-a', '--archive', help='archive messages to disk', action='store_true')
    parser.add_argument('-d', '--delete', help='delete messages', action='store_true')

    args = parser.parse_args()

    if args.help:
        parser.print_help()
        exit(0)

    logging.info("Running operator... %s", args)
    search_expr = ' '.join(args.search_expr)

    if args.delete:
        delete_messages(search_expr, args.max)
    elif args.archive:
        raise Exception('Not Implemented YET!')
    else:
        preview_messages(search_expr, args.max)
