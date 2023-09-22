import json
from typing import Any, Dict, Optional
from urllib.parse import urlunparse, urlparse

from talkylabs.reach.base.exceptions import ReachException
from talkylabs.reach.http.response import Response


class Page(object):
    """
    Represents a page of records in a collection.

    A `Page` lets you iterate over its records and fetch the next and previous
    pages in the collection.
    """

    META_KEYS = {
        "outOfPageRange",
        "page",
        "pageSize",
        "totalPages",
        "page",
    }

    def __init__(self, url, version, response: Response, solution={}):
        payload = self.process_response(response)

        self._version = version
        self._payload = payload
        self._solution = solution
        self._records = iter(self.load_page(payload))
        self._url = url

    def __iter__(self):
        """
        A `Page` is a valid iterator.
        """
        return self

    def __next__(self):
        return self.next()

    def next(self):
        """
        Returns the next record in the `Page`.
        """
        return self.get_instance(next(self._records))

    @classmethod
    def process_response(cls, response: Response) -> Any:
        """
        Load a JSON response.

        :param response: The HTTP response.
        :return The JSON-loaded content.
        """
        if response.status_code != 200:
            raise ReachException("Unable to fetch page", response)

        return json.loads(response.text)

    def load_page(self, payload: Dict[str, Any]):
        """
        Parses the collection of records out of a list payload.

        :param payload: The JSON-loaded content.
        :return list: The list of records.
        """
        if "meta" in payload and "key" in payload["meta"]:
            return payload[payload["meta"]["key"]]
        else:
            keys = set(payload.keys())
            key = keys - self.META_KEYS
            if len(key) == 1:
                return payload[key.pop()]
            elif len(key) == 2:
                key1, key2 = list(key)
                dataKey = key1 if len(key1) < len(key2) else key2
                otherKey = key1 if dataKey == key2 else key2
                checkKey = "total" + dataKey[0].upper() + dataKey[1:]
                if checkKey == otherKey:
                    return payload[dataKey]

        raise ReachException("Page Records can not be deserialized")

    @property
    def previous_page_url(self) -> Optional[str]:
        """
        :return str: Returns a link to the previous_page_url or None if doesn't exist.
        """
        current_page = self._payload["page"] if "page" in self._payload else 0
        page_size = self._payload["pageSize"] if "pageSize" in self._payload else 1
        if current_page > 0:
            parsed = urlparse(self._url)
            query = f"pageSize={page_size}&page={current_page-1}"
            if not ((parsed.query is None) or len(parsed.query) == 0):
                query = parsed.query + "&" + query
            r = parsed._replace(query=query)
            return urlunparse(r)

        return None

    @property
    def next_page_url(self) -> Optional[str]:
        """
        :return str: Returns a link to the next_page_url or None if doesn't exist.
        """
        current_page = self._payload["page"] if "page" in self._payload else 0
        page_size = self._payload["pageSize"] if "pageSize" in self._payload else 1
        outOfPageRange = self._payload["outOfPageRange"] if "outOfPageRange" in self._payload else True
        totalPages = self._payload["totalPages"] if "totalPages" in self._payload else 1
        if not (outOfPageRange or (current_page + 1 >= totalPages)):
            query = f"pageSize={page_size}&page={current_page+1}"
            parsed = urlparse(self._url)
            if not ((parsed.query is None) or len(parsed.query) == 0):
                query = parsed.query + "&" + query
            r = parsed._replace(query=query)
            return urlunparse(r)

        return None

    def get_instance(self, payload: Dict[str, Any]) -> Any:
        """
        :param dict payload: A JSON-loaded representation of an instance record.
        :return: A rich, resource-dependent object.
        """
        raise ReachException(
            "Page.get_instance() must be implemented in the derived class"
        )

    def next_page(self) -> Optional["Page"]:
        """
        Return the `Page` after this one.
        :return The next page.
        """
        if not self.next_page_url:
            return None

        response = self._version.domain.reach.request("GET", self.next_page_url)
        cls = type(self)
        return cls(self._url, self._version, response, self._solution)

    async def next_page_async(self) -> Optional["Page"]:
        """
        Asynchronously return the `Page` after this one.
        :return The next page.
        """
        if not self.next_page_url:
            return None

        response = await self._version.domain.reach.request_async(
            "GET", self.next_page_url
        )
        cls = type(self)
        return cls(self._url, self._version, response, self._solution)

    def previous_page(self) -> Optional["Page"]:
        """
        Return the `Page` before this one.
        :return The previous page.
        """
        if not self.previous_page_url:
            return None

        response = self._version.domain.reach.request("GET", self.previous_page_url)
        cls = type(self)
        return cls(self._url, self._version, response, self._solution)

    async def previous_page_async(self) -> Optional["Page"]:
        """
        Asynchronously return the `Page` before this one.
        :return The previous page.
        """
        if not self.previous_page_url:
            return None

        response = await self._version.domain.reach.request_async(
            "GET", self.previous_page_url
        )
        cls = type(self)
        return cls(self._url, self._version, response, self._solution)

    def __repr__(self) -> str:
        return "<Page>"
