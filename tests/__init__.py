import unittest

from tests.holodeck import Holodeck
from talkylabs.reach.rest import ReachClient


class IntegrationTestCase(unittest.TestCase):
    def setUp(self):
        super(IntegrationTestCase, self).setUp()
        self.api_user = "XX" + "a" * 32
        self.api_key = "AUTHTOKEN"
        self.holodeck = Holodeck()
        self.client = ReachClient(
            username=self.api_user,
            password=self.api_key,
            http_client=self.holodeck,
        )
