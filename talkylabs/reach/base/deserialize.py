import datetime
from decimal import BasicContext, Decimal
from email.utils import parsedate
from typing import Optional, Union

import pytz

ISO8601_DATE_FORMAT = "%Y-%m-%d"
ISO8601_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
RFC3339_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


def iso8601_date(s: str) -> Optional[Union[datetime.date, str]]:
    """
    Parses an ISO 8601 date string and returns a UTC date object or the string
    if the parsing failed.
    :param s: ISO 8601-formatted date string (2015-01-25)
    :return:
    """
    try:
        return (
            datetime.datetime.strptime(s, ISO8601_DATE_FORMAT)
            .replace(tzinfo=pytz.utc)
            .date()
        )
    except (TypeError, ValueError):
        return s


def iso8601_datetime(
    s: str,
) -> Optional[Union[datetime.datetime, str]]:
    """
    Parses an ISO 8601 datetime string and returns a UTC datetime object,
    or the string if parsing failed.
    :param s: ISO 8601-formatted datetime string (2015-01-25T12:34:56Z)
    """
    try:
        return datetime.datetime.strptime(s, ISO8601_DATETIME_FORMAT).replace(
            tzinfo=pytz.utc
        )
    except (TypeError, ValueError):
        try:
            return datetime.datetime.strptime(s, RFC3339_DATETIME_FORMAT).replace(
                tzinfo=pytz.utc
            )
        except (TypeError, ValueError):
            return s


def rfc2822_datetime(s: str) -> Optional[datetime.datetime]:
    """
    Parses an RFC 2822 date string and returns a UTC datetime object,
    or the string if parsing failed.
    :param s: RFC 2822-formatted string date
    :return: datetime or str
    """
    date_tuple = parsedate(s)
    if date_tuple is None:
        return None
    return datetime.datetime(*date_tuple[:6]).replace(tzinfo=pytz.utc)


def decimal(d: Optional[str]) -> Optional[Union[Decimal, str]]:
    """
    Parses a decimal string into a Decimal
    :param d: decimal string
    """
    if not d:
        return d
    return Decimal(d, BasicContext)


def integer(i: str) -> Optional[Union[int, str]]:
    """
    Parses an integer string into an int
    :param i: integer string
    :return: int
    """
    try:
        return int(i)
    except (TypeError, ValueError):
        return i
