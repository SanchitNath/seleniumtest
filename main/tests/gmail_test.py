# pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

import pytest
import base64
from email.mime.text import MIMEText
from google.oauth2 import service_account
from googleapiclient.discovery import build


@pytest.mark.GmailService
class GmailService:
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    SERVICE_ACCOUNT_FILE = 'path/to/your/service-account-file.json'
    IMPERSONATED_USER = 'test_user@testdomain.com'

    def __init__(self):
        # Base credentials from the JSON file
        base_credentials = service_account.Credentials.from_service_account_file(
            self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES)

        # Delegate authority to act as the actual workspace user
        self.credentials = base_credentials.with_subject(self.IMPERSONATED_USER)
        self.service = build('gmail', 'v1', credentials=self.credentials)

    def test_send_email(self, to: str, subject: str, body: str):
        message = MIMEText(body)
        message['to'] = to
        message['subject'] = subject
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        try:
            message = self.service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
            print(f'Message Id: {message["id"]}')
            return message
        except Exception as e:
            print(f'An error occurred: {e}')
            return None


# gmail = GmailService()
# message = gmail.test_send_email("recipient@testdomain.com", "Hello!", "This is a test email.")
# assert message is not None, "Failed to send email"
