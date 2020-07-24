#!/usr/local/bin/python3.7
from process_request import RequestApartments
from notification import notifiy
import argparse
import json


def main(link, sender):

    """ Main function
    :type link: str
    :param link: query link

    :type sender: str
    :param sender: email address of the sender

    :raises:

    :rtype:
    """

    r = RequestApartments()
    new_apartments = r.run(link)
    if not new_apartments or len(new_apartments) == 0:
        return
    notifiy(
        sender=sender,
        to=sender,
        subject="New apartment notification",
        message_text=json.dumps(new_apartments, indent=4, sort_keys=True)
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--addr", required=True, type=str)
    parser.add_argument("--sender", required=True, type=str)
    args = parser.parse_args()
    main(args.addr, args.sender)
