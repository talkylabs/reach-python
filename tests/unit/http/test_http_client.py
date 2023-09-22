# -*- coding: utf-8 -*-
import os
import unittest
from collections import OrderedDict

from mock import Mock, patch
from requests import Session

from talkylabs.reach.base.exceptions import ReachRestException
from talkylabs.reach.base.version import Version
from talkylabs.reach.http.http_client import ReachHttpClient
from talkylabs.reach.http.response import Response


class TestHttpClientRequest(unittest.TestCase):
    def setUp(self):
        self.session_patcher = patch("talkylabs.reach.http.http_client.Session")

        self.session_mock = Mock(wraps=Session())
        self.request_mock = Mock()

        self.session_mock.prepare_request.return_value = self.request_mock
        self.session_mock.send.return_value = Response(200, "testing-unicode: Ω≈ç√, 💩")
        self.request_mock.headers = {}

        session_constructor_mock = self.session_patcher.start()
        session_constructor_mock.return_value = self.session_mock

        self.client = ReachHttpClient()

    def tearDown(self):
        self.session_patcher.stop()

    def test_request_sets_host_header_if_missing(self):
        self.request_mock.url = "https://api.reach.talkylabs.com/"
        self.request_mock.headers = {"Host": "other.reach.talkylabs.com"}

        self.client.request("doesnt matter", "doesnt matter")

        self.assertEqual("other.reach.talkylabs.com", self.request_mock.headers["Host"])
        self.assertIsNotNone(self.client._test_only_last_request)
        self.assertIsNotNone(self.client._test_only_last_response)

    def test_request_with_timeout(self):
        self.request_mock.url = "https://api.reach.talkylabs.com/"
        self.request_mock.headers = {"Host": "other.reach.talkylabs.com"}

        response = self.client.request(
            "doesnt matter", "doesnt matter", None, None, None, None, 30
        )

        self.assertEqual("other.reach.talkylabs.com", self.request_mock.headers["Host"])
        self.assertEqual(200, response.status_code)
        self.assertEqual("testing-unicode: Ω≈ç√, 💩", response.content)

    def test_request_where_method_timeout_equals_zero(self):
        self.request_mock.url = "https://api.reach.talkylabs.com/"
        self.request_mock.headers = {"Host": "other.reach.talkylabs.com"}

        try:
            self.client.request(
                "doesnt matter", "doesnt matter", None, None, None, None, 0
            )
        except Exception as e:
            self.assertEqual(ValueError, type(e))

    def test_request_where_class_timeout_manually_set(self):
        self.request_mock.url = "https://api.reach.talkylabs.com/"
        self.request_mock.headers = {"Host": "other.reach.talkylabs.com"}
        self.client.timeout = 30

        response = self.client.request("doesnt matter", "doesnt matter")
        self.assertEqual("other.reach.talkylabs.com", self.request_mock.headers["Host"])
        self.assertEqual(200, response.status_code)
        self.assertEqual("testing-unicode: Ω≈ç√, 💩", response.content)

    def test_request_where_class_timeout_equals_zero(self):
        self.request_mock.url = "https://api.reach.talkylabs.com/"
        self.request_mock.headers = {"Host": "other.reach.talkylabs.com"}
        self.client.timeout = 0

        try:
            self.client.request("doesnt matter", "doesnt matter")
        except Exception as e:
            self.assertEqual(type(e), ValueError)

    def test_request_where_class_timeout_and_method_timeout_set(self):
        self.request_mock.url = "https://api.reach.talkylabs.com/"
        self.request_mock.headers = {"Host": "other.reach.talkylabs.com"}
        self.client.timeout = 30

        response = self.client.request(
            "doesnt matter", "doesnt matter", None, None, None, None, 15
        )

        self.assertEqual("other.reach.talkylabs.com", self.request_mock.headers["Host"])
        self.assertEqual(200, response.status_code)
        self.assertEqual("testing-unicode: Ω≈ç√, 💩", response.content)

    def test_request_with_unicode_response(self):
        self.request_mock.url = "https://api.reach.talkylabs.com/"
        self.request_mock.headers = {"Host": "other.reach.talkylabs.com"}

        response = self.client.request("doesnt matter", "doesnt matter")

        self.assertEqual("other.reach.talkylabs.com", self.request_mock.headers["Host"])
        self.assertEqual(200, response.status_code)
        self.assertEqual("testing-unicode: Ω≈ç√, 💩", response.content)

    def test_last_request_last_response_exist(self):
        self.request_mock.url = "https://api.reach.talkylabs.com/"
        self.request_mock.headers = {"Host": "other.reach.talkylabs.com"}

        self.client.request(
            "doesnt-matter-method",
            "doesnt-matter-url",
            {"params-value": "params-key"},
            {"data-value": "data-key"},
            {"headers-value": "headers-key"},
            ["a", "b"],
        )

        self.assertIsNotNone(self.client._test_only_last_request)
        self.assertEqual("doesnt-matter-url", self.client._test_only_last_request.url)
        self.assertEqual(
            "DOESNT-MATTER-METHOD", self.client._test_only_last_request.method
        )
        self.assertEqual(
            {"params-value": "params-key"}, self.client._test_only_last_request.params
        )
        self.assertEqual(
            {"data-value": "data-key"}, self.client._test_only_last_request.data
        )
        self.assertEqual(
            {"headers-value": "headers-key", "ApiUser": "a", "ApiKey": "b"},
            self.client._test_only_last_request.headers,
        )
        self.assertEqual(None, self.client._test_only_last_request.auth)

        self.assertIsNotNone(self.client._test_only_last_response)

        if self.client._test_only_last_response is not None:
            self.assertEqual(200, self.client._test_only_last_response.status_code)
            self.assertEqual(
                "testing-unicode: Ω≈ç√, 💩", self.client._test_only_last_response.text
            )

    def test_last_response_empty_on_error(self):
        self.session_mock.send.side_effect = Exception("voltron")

        with self.assertRaises(Exception):
            self.client.request("doesnt-matter", "doesnt-matter")

            self.assertIsNotNone(self.client._test_only_last_request)
            self.assertIsNone(self.client._test_only_last_response)

    def test_request_behind_proxy(self):
        self.request_mock.url = "https://api.reach.talkylabs.com/"
        proxies = OrderedDict(
            [
                ("http", "http://proxy.reach.talkylabs.com"),
                ("https", "https://proxy.reach.talkylabs.com"),
            ]
        )
        self.client = ReachHttpClient(proxy=proxies)
        self.client.request("doesnt matter", "doesnt matter")
        self.session_mock.send.assert_called_once_with(
            self.request_mock,
            verify=True,
            proxies=proxies,
            stream=False,
            cert=None,
            allow_redirects=False,
            timeout=None,
        )

    @patch.dict(
        os.environ,
        {
            "HTTP_PROXY": "http://proxy.reach.talkylabs.com",
            "HTTPS_PROXY": "https://proxy.reach.talkylabs.com",
        },
    )
    def test_request_behind_proxy_from_environment(self):
        self.request_mock.url = "https://api.reach.talkylabs.com/"
        self.client = ReachHttpClient()
        self.client.request("doesnt matter", "doesnt matter")
        self.session_mock.send.assert_called_once_with(
            self.request_mock,
            verify=True,
            proxies=OrderedDict(
                [
                    ("http", "http://proxy.reach.talkylabs.com"),
                    ("https", "https://proxy.reach.talkylabs.com"),
                ]
            ),
            stream=False,
            cert=None,
            allow_redirects=False,
            timeout=None,
        )

    def test_exception_with_details(self):
        self.request_mock.url = "https://api.reach.talkylabs.com/"
        v1 = MyVersion(self.client)
        error_text = """{
            "errorCode": 20001,
            "errorMessage": "Bad request",
            "more_info": "https://www.reach.talkylabs.com/docs/errors/20001",
            "status": 400,
            "errorDetails": {
                "foo":"bar"
            }
        }"""
        self.session_mock.send.return_value = Response(400, error_text)
        try:
            v1.fetch("get", "none", None, None, None, None, None)
            self.fail("should not happen")
        except ReachRestException as err:
            self.assertEqual(400, err.status)
            self.assertEqual(20001, err.code)
            self.assertEqual("get", err.method)
            self.assertEqual("Unable to fetch record: Bad request", err.msg)
            self.assertEqual({"foo": "bar"}, err.details)


class TestHttpClientSession(unittest.TestCase):
    def setUp(self):
        self.session_patcher = patch("talkylabs.reach.http.http_client.Session")
        self.session_constructor_mock = self.session_patcher.start()

    def tearDown(self):
        self.session_patcher.stop()

    def _setup_session_response(self, value):
        session_mock = Mock(wraps=Session())
        request_mock = Mock(url="https://api.reach.talkylabs.com/")

        session_mock.prepare_request.return_value = request_mock
        session_mock.send.return_value = Response(200, value)
        self.session_constructor_mock.return_value = session_mock

    def test_session_preserved(self):
        self._setup_session_response("response_1")

        client = ReachHttpClient()
        response_1 = client.request("GET", "https://api.reach.talkylabs.com")

        self._setup_session_response("response_2")
        response_2 = client.request("GET", "https://api.reach.talkylabs.com")

        # Used same session, response should be the same
        self.assertEqual(response_1.content, "response_1")
        self.assertEqual(response_2.content, "response_1")

    def test_session_not_preserved(self):
        self._setup_session_response("response_1")

        client = ReachHttpClient(pool_connections=False)
        response_1 = client.request("GET", "https://api.reach.talkylabs.com")

        self._setup_session_response("response_2")
        response_2 = client.request("GET", "https://api.reach.talkylabs.com")

        # Used different session, responses should be different
        self.assertEqual(response_1.content, "response_1")
        self.assertEqual(response_2.content, "response_2")


class MyVersion(Version):
    def __init__(self, domain):
        super().__init__(domain, "v1")
        self._credentials = None
