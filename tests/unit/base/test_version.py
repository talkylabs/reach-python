from tests import IntegrationTestCase
from tests.holodeck import Request
from talkylabs.reach.base.page import Page
from talkylabs.reach.http.response import Response


class MyTestPage(Page):
    def get_instance(self, payload):
        return payload


class StreamTestCase(IntegrationTestCase):
    def setUp(self):
        super(StreamTestCase, self).setUp()

        self.holodeck.mock(
            Response(
                200,
                """{
                    "page": 0,
                    "pageSize": 2,
                    "totalPages": 3,
                    "outOfPageRange": false,
                    "totalMessages": 5,
                    "messages": [{"body": "payload0"}, {"body": "payload1"}]
                }""",
            ),
            Request(
                url="https://api.reach.talkylabs.com/rest/messaging/v1/list"
            ),
        )

        self.holodeck.mock(
            Response(
                200,
                """{
                    "page": 1,
                    "pageSize": 2,
                    "totalPages": 3,
                    "outOfPageRange": false,
                    "totalMessages": 5,
                    "messages": [{"body": "payload2"}, {"body": "payload3"}]
                }""",
            ),
            Request(
                url="https://api.reach.talkylabs.com/rest/messaging/v1/list?pageSize=2&page=1"
            ),
        )

        self.holodeck.mock(
            Response(
                200,
                """{
                    "page": 2,
                    "pageSize": 2,
                    "totalPages": 3,
                    "outOfPageRange": true,
                    "totalMessages": 5,
                    "messages": [{"body": "payload4"}]
                }""",
            ),
            Request(
                url="https://api.reach.talkylabs.com/rest/messaging/v1/list?pageSize=2&page=2"
            ),
        )

        self.version = self.client.messaging
        self.response = self.version.page(
            method="GET", uri="/messaging/v1/list"
        )
        url = self.version.url_without_pagination_info(url="https://api.reach.talkylabs.com/rest/messaging/v1/list")
        self.page = MyTestPage(url, self.version, self.response, {})

    def test_stream(self):
        messages = list(self.version.stream(self.page))

        self.assertEqual(len(messages), 5)

    def test_stream_limit(self):
        messages = list(self.version.stream(self.page, limit=3))

        self.assertEqual(len(messages), 3)

    def test_stream_page_limit(self):
        messages = list(self.version.stream(self.page, page_limit=1))

        self.assertEqual(len(messages), 2)


class VersionTestCase(IntegrationTestCase):
    def test_fetch_redirect(self):
        self.holodeck.mock(
            Response(307, '{"redirect_to": "some_place"}'),
            Request(url="https://api.reach.talkylabs.com/rest/Deactivations"),
        )
        response = self.client.messaging.fetch(method="GET", uri="/Deactivations")

        self.assertIsNotNone(response)
