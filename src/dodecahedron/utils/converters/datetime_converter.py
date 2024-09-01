# -*- coding: utf-8 -*-
"""Datetime Converter.

Module provides function for converting values to datatimes.

"""

# Standard Library Imports
from datetime import date
from datetime import datetime
from datetime import tzinfo
import logging
from typing import Optional

# Third-Party Imports
import cachetools
from cachetools.keys import hashkey
from dateutil.parser import parse
from dateutil.parser import ParserError
from dateutil.tz import tzlocal
import pytz

__all__ = ["to_datetime", "to_naive_datetime"]


# Initialize logger.
log = logging.getLogger("dodecahedron")


def to_datetime(
    __value: object,
    /,
    default: Optional[datetime] = None,
    tz: tzinfo = pytz.utc,
) -> Optional[datetime]:
    """Convert value to datetime.

    Args:
        __value: Value to convert to datetime.
        default (optional): Default value. Default ``None``.
        tz (optional): Timezone. Default `UTC`.

    Returns:
        Datetime.

    Raises:
        ValueError: when value cannot be converted to datetime.

    """
    if __value is None:
        dt = default

    elif isinstance(__value, datetime):
        dt = __value

    elif isinstance(__value, date):
        dt = _from_date(__value)

    elif isinstance(__value, str):
        dt = _from_string(__value)

    else:
        raise ValueError(f"{type(__value)} cannot be converted to datetime")

    result = _as_utc_timezone(dt) if dt is not None else default
    return result


def _from_date(__value: object, /) -> datetime:
    """Converts date value to datetime.

    Args:
        __value: Date.

    Raises:
        TypeError: when value is not type 'date'.

    """
    if not isinstance(__value, date):
        message = f"expected type 'date', got {type(__value)} instead"
        raise TypeError(message)

    result = datetime.combine(__value, datetime.min.time())
    return result


@cachetools.cached(cachetools.LRUCache(maxsize=1000), hashkey)
def _from_string(
    __value: object, /, default: Optional[datetime] = None
) -> Optional[datetime]:
    """Converts string value to datetime.

    Args:
        __value: String representation of datetime.
        default (optional): Default value. Default ``None``.

    Raises:
        TypeError: when value is not type 'str'.

    """
    if not isinstance(__value, str):
        message = f"expected type 'str', got {type(__value)} instead"
        raise TypeError(message)

    try:
        value = __value.replace("  ", " ").strip()
        result = parse(value) if value else default

    except (ParserError, ValueError):
        log.warn("Cannot convert '%s' to datetime", __value)
        result = default

    return result


def _as_utc_timezone(__value: datetime, /) -> datetime:
    """Set to UTC timezone.

    Args:
        __value: Datetime on which to set UTC timezone.

    Returns:
        Datetime with UTC timezone.

    Raises:
        TypeError: when value is not type 'datetime'.

    """
    if not isinstance(__value, datetime):
        message = f"expected type 'datetime', got {type(__value)} instead"
        raise TypeError(message)

    if __value.tzinfo is None or __value.tzinfo.utcoffset(__value) is None:
        __value = _add_local_timezone(__value)

    result = __value.astimezone(pytz.utc)
    return result


def _add_local_timezone(__value: datetime, /) -> datetime:
    """Add local timezone to datetime.

    Args:
        value: Datetime to which to add timezone.

    Returns:
        Datetime with timezone.

    Raises:
        TypeError: when value is not type 'datetime'.

    """
    if not isinstance(__value, datetime):
        message = f"expected type 'datetime', got {type(__value)} instead"
        raise TypeError(message)

    timezone = pytz.timezone(tzlocal().tzname)
    result = timezone.localize(__value)
    return result


def to_naive_datetime(__date: date, /) -> datetime:
    """Convert date to naive datetime.

    Args:
        __date: Date to convert to datetime.

    Returns:
        Datetime.

    """
    if not isinstance(__date, date):
        message = f"expected type 'date', got {type(__date)} instead"
        raise TypeError(message)

    value = __date.date() if isinstance(__date, datetime) else __date
    result = datetime.combine(value, datetime.min.time())
    return result
