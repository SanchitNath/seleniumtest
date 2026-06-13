import pytest
import os
from main.pages.flipkart_page import Flipkart

@pytest.mark.FlipkartTest
@pytest.mark.FlipkartTest1
class TestFlipkart:

    def setup_method(self):
        print("In setup method")
        print(os.path.basename(__file__))
        print(os.path.splitext(os.path.basename(__file__)))
        print("_________")
        self.fp = Flipkart(self)

    def test_flipkart(self):
        self.logger.info("Starting the Flipkart test case.")
        self.logger.debug("This is a DEBUG message")
        self.logger.warning("This is a WARNING message")
        self.logger.error("This is an ERROR message")
        self.logger.critical("This is an CRITICAL message")
        self.fp.auth_and_signup(os.getenv('URL'), os.getenv('CONTACT'))
