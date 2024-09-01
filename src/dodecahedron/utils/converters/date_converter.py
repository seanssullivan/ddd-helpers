# -*- coding: utf-8 -*-
"""Date Converter.

Module provides function for converting values to dates.

"""

# Standard Library Imports
import datetime
import logging
from typing import Optional

# Third-Party Imports
# import cachetools
# from cachetools.keys import hashkey
# from dateutil.parser import parse

# from dateutil.parser import ParserError

__all__ = ["to_date"]


# Initialize logger.
log = logging.getLogger("dodecahedron")


def to_date(
    __value: object, /, default: Optional[datetime.date] = None
) -> Optional[datetime.date]:
    """Converts value to date.

    Args:
        __value: Date.
        default (optional): Default value. Default ``None``.

    Returns:
        Date.

    Raises:
        ValueError: when value cannot be converted to date.

    """
    if __value is None:
        return default

    if isinstance(__value, datetime.datetime):
        return __value.date()

    if isinstance(__value, datetime.date):
        return __value

    # if isinstance(__value, str):
    #     return _from_string(__value, default)

    raise TypeError(f"{type(__value)} cannot be converted to date")


# @cachetools.cached(cachetools.LRUCache(maxsize=1000), hashkey)
# def _from_string(
#     __value: str, /, default: Optional[datetime.date] = None
# ) -> Optional[datetime.date]:
#     """Converts string value to date.

#     Args:
#         __value: String representation of date.
#         default (optional): Default value. Default ``None``.

#     Raises:
#         TypeError: when value is not type 'str'.

#     """
#     if not isinstance(__value, str):
#         message = f"expected type 'str', got {type(__value)} instead"
#         raise TypeError(message)

#     try:
#         value = __value.replace("  ", " ").strip()
#         result = parse(value).date() if value else default

#     except (ParserError, ValueError):
#         log.warn("Cannot convert '%s' to date", __value)
#         result = default

#     return result
