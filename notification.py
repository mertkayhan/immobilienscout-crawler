from email.mime.text import MIMEText
import base64
from googleapiclient.errors import HttpError
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from contextlib import contextmanager
import logging

logging.basicConfig(filename='search-apartment.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s',
                    level=0)


def __create_message(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

    Returns:
    An object containing a base64url encoded email object.
    """

    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    return {'raw': base64.urlsafe_b64encode(
        message.as_string().encode("utf-8")
        ).decode("utf-8")}


def __send_message(service, user_id, message):
    """Send an email message.

    Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    message: Message to be sent.

    Returns:
    Sent Message.
    """

    try:
        message = (service.users().messages().send(userId=user_id,
                                                   body=message).execute())
        logging.info('Message Id: %s' % message['id'])
        return message
    except HttpError as error:
        logging.error('An error occurred: %s' % error)


@contextmanager
def __notification_manager():
    """ Context manager for email notifications. Initiates the connection
        and checks the authentication.

    :rtype:
    Yields the Gmail service.
    """

    SCOPES = ['https://mail.google.com/']
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)
    logging.info("Connection to Gmail API established.")
    yield service
    logging.info("Sent the notification email.")


def notifiy(sender, to, subject, message_text):

    msg = __create_message(
                sender=sender,
                to=to,
                subject=subject,
                message_text=message_text
                )

    with __notification_manager() as service:
        __send_message(
              service=service,
              user_id=sender,
              message=msg
              )


if __name__ == "__main__":
    pass
