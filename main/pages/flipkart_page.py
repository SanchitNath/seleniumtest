import os

import allure
import requests
from main.pages.base_page import BasePage


class Flipkart(BasePage):
    def __init__(self, test_instance):
        super().__init__(test_instance)
        print("Inside class")
        print(os.environ['URL'])
        print("---->>")
        self.session = requests.Session()
        url = os.getenv('URL')
        contact = os.getenv('CONTACT')
        signup_url = os.getenv('SIGN_UP_URL')
        print("from os.getenv() <---->")
        self.logger.info(url)
        self.logger.info(contact)
        self.logger.info(signup_url)

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*'
        }

    def handle_status(self, response, stage: str):
        code = response.status_code
        if code == 200:
            self.logger.info(f"{stage} Successful (200)")
            return True
        elif code == 400:
            self.logger.error(f"{stage} Failed: Bad Request (400). Check your payload or URL parameters.")
        elif code == 401:
            self.logger.error(f"{stage} Failed: Unauthorized (401). Your credentials or headers might be wrong.")
        else:
            self.logger.error(f"{stage} returned status: {code} with text={response.text}")
        return False

    @allure.title("Auth and then Signup")
    def auth_and_signup(self, url: str, contact: str):
        url_auth_resp = self.session.get(
            url,
            headers=self.headers
        )
        self.logger.info(f"Auth isn't returning auth token as they use cookies")
        self.logger.info(f"{url_auth_resp} of type {type(url_auth_resp)}")
        if not self.handle_status(url_auth_resp, "URL Auth"):
            return

        login_payload = {
            "loginId": [str(contact)],
            "supportAllStates": True
        }
        login_resp = self.session.post(
            os.environ.get('SIGN_UP_URL'),
            json=login_payload,
            # headers=self.headers,
        )
        print(login_resp)
        self.handle_status(login_resp, "Signup/Post")