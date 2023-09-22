import unittest
import aiounittest

from mock import AsyncMock, Mock, patch
from requests import Session

from talkylabs.reach.http.response import Response
from talkylabs.reach.rest import ReachClient



class TestUserAgentClients(unittest.TestCase):
    def setUp(self):
        self.session_patcher = patch("talkylabs.reach.http.http_client.Session")

        self.session_mock = Mock(wraps=Session())
        self.request_mock = Mock()

        self.session_mock.prepare_request.return_value = self.request_mock
        self.session_mock.send.return_value = Response(200, "testing-unicode: Ω≈ç√, 💩")
        self.request_mock.headers = {}

        session_constructor_mock = self.session_patcher.start()
        session_constructor_mock.return_value = self.session_mock


        self.client = ReachClient("username", "password")

    def tearDown(self):
        self.client.http_client.session.close()

    def test_set_default_user_agent(self):
        self.request_mock.url = "https://api.reach.talkylabs.com/"
        self.client.request("GET", "https://api.reach.talkylabs.com/")
        request_header = self.client.http_client._test_only_last_request.headers[
            "User-Agent"
        ]
        self.assertRegex(
            request_header,
            r"^reach-python\/[0-9.]+(-rc\.[0-9]+)?\s\(\w+\s\w+\)\sPython\/[^\s]+$",
        )

    def test_set_user_agent_extensions(self):
        self.request_mock.url = "https://api.reach.talkylabs.com/"
        expected_user_agent_extensions = ["reach-run/2.0.0-test", "flex-plugin/3.4.0"]
        self.client.user_agent_extensions = expected_user_agent_extensions
        self.client.request("GET", "https://api.reach.talkylabs.com/")
        user_agent_headers = self.client.http_client._test_only_last_request.headers[
            "User-Agent"
        ]
        user_agent_extensions = user_agent_headers.split(" ")[
            -len(expected_user_agent_extensions) :
        ]
        self.assertEqual(user_agent_extensions, expected_user_agent_extensions)


class TestClientAsyncRequest(aiounittest.AsyncTestCase):
    def setUp(self):
        self.mock_async_http_client = AsyncMock()
        self.mock_async_http_client.request.return_value = Response(200, "test")
        self.mock_async_http_client.is_async = True
        self.client = ReachClient(
            "username", "password", http_client=self.mock_async_http_client
        )

    async def test_raise_error_if_client_not_marked_async(self):
        mock_http_client = Mock()
        mock_http_client.request.return_value = Response(200, "doesnt matter")
        mock_http_client.is_async = None

        client = ReachClient("username", "password", http_client=mock_http_client)
        with self.assertRaises(RuntimeError):
            await client.request_async("doesnt matter", "doesnt matter")

    async def test_raise_error_if_client_is_not_async(self):
        mock_http_client = Mock()
        mock_http_client.request.return_value = Response(200, "doesnt matter")
        mock_http_client.is_async = False

        client = ReachClient("username", "password", http_client=mock_http_client)
        with self.assertRaises(RuntimeError):
            await client.request_async("doesnt matter", "doesnt matter")

    async def test_request_async_called_with_method_and_url(self):
        await self.client.request_async("GET", "http://mock.reach.talkylabs.com")
        self.assertEqual(self.mock_async_http_client.request.call_args.args[0], "GET")
        self.assertEqual(
            self.mock_async_http_client.request.call_args.args[1],
            "http://mock.reach.talkylabs.com",
        )
