import os
import unittest

from talkylabs.reach.rest import ReachClient


class ClusterTest(unittest.TestCase):
    def setUp(self):
        self.from_number = os.environ["REACH_TALKYLABS_FROM_NUMBER"]
        self.to_number = os.environ["REACH_TALKYLABS_TO_NUMBER"]
        self.api_key = os.environ["REACH_TALKYLABS_API_KEY"]
        self.api_user = os.environ["REACH_TALKYLABS_API_USER"]
        self.client = ReachClient(
            username=self.api_user,
            password=self.api_key,
        )

    def test_send_text_message(self):
        msg = self.client.messages.create(
            to=self.to_number, from_=self.from_number, body="hello world"
        )
        self.assertEqual(msg.to, self.to_number)
        self.assertEqual(msg._from, self.from_number)
        self.assertEqual(msg.body, "hello world")
        self.assertIsNotNone(msg.sid)

