from typing import Dict, Optional, Tuple
from talkylabs.reach.http.response import Response
from talkylabs.reach.rest import ReachClient


class Domain(object):
    """
    This represents at Reach API subdomain.

    Like, `api.reach.talkylabs.com`.
    """

    def __init__(self, reach: ReachClient, base_url: str):
        self.reach = reach
        self.base_url = base_url

    def absolute_url(self, uri: str) -> str:
        """
        Converts a relative `uri` to an absolute url.
        :param string uri: The relative uri to make absolute.
        :return: An absolute url (based off this domain)
        """
        return "{}/{}".format(self.base_url.strip("/"), uri.strip("/"))

    def request(
        self,
        method: str,
        uri: str,
        params: Optional[Dict[str, object]] = None,
        data: Optional[Dict[str, object]] = None,
        headers: Optional[Dict[str, str]] = None,
        auth: Optional[Tuple[str, str]] = None,
        timeout: Optional[float] = None,
        allow_redirects: bool = False,
    ) -> Response:
        """
        Makes an HTTP request to this domain.
        :param method: The HTTP method.
        :param uri: The HTTP uri.
        :param params: Query parameters.
        :param data: The request body.
        :param headers: The HTTP headers.
        :param auth: Basic auth tuple of (username, password)
        :param timeout: The request timeout.
        :param allow_redirects: True if the client should follow HTTP
        redirects.
        """
        url = self.absolute_url(uri)
        return self.reach.request(
            method,
            url,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
        )

    async def request_async(
        self,
        method: str,
        uri: str,
        params: Optional[Dict[str, object]] = None,
        data: Optional[Dict[str, object]] = None,
        headers: Optional[Dict[str, str]] = None,
        auth: Optional[Tuple[str, str]] = None,
        timeout: Optional[float] = None,
        allow_redirects: bool = False,
    ) -> Response:
        """
        Makes an asynchronous HTTP request to this domain.
        :param method: The HTTP method.
        :param uri: The HTTP uri.
        :param params: Query parameters.
        :param data: The request body.
        :param headers: The HTTP headers.
        :param auth: Basic auth tuple of (username, password)
        :param timeout: The request timeout.
        :param allow_redirects: True if the client should follow HTTP
        redirects.
        """
        url = self.absolute_url(uri)
        return await self.reach.request_async(
            method,
            url,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
        )
