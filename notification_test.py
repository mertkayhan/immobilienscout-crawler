import unittest
from notification import notifiy


class TestNofication(unittest.TestCase):

    def test_notify(self):

        addr = input("Please enter your email address: ")
        notifiy(
            sender=addr,
            to=addr,
            subject="Test message",
            message_text="This is a test message."
        )


if __name__ == '__main__':
    unittest.main()
