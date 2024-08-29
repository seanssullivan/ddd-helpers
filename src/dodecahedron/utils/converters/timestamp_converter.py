# -*- coding: utf-8 -*-
"""Timestamp Converter.

Module provides function for converting values to timestamps.

"""

# Standard Library Imports
from datetime import date
import time

__all__ = ["to_timestamp"]


def to_timestamp(__date: date, /) -> float:
    """Convert date to timestamp.

    Args:
        __date: Date to convert to timestamp.

    Returns:
        Timestamp.
    """
    if not isinstance(__date, date):
        message = f"expected type 'date', got {type(__date)} instead"
        raise TypeError(message)

    result = time.mktime(__date.timetuple())
    return result
