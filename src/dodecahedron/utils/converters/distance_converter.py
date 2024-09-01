# -*- coding: utf-8 -*-
"""Distance Converter.

Module provides functions for converting values to distances.

"""

# Standard Library Imports
import re

__all__ = ["to_distance"]


def to_distance(__value: object, /, default: float = 0.0) -> float:
    """Convert value to distance.

    Args:
        __value: Value to convert to distance.
        default (optional): Default value. Default ``0.0``.

    Raises:
        ValueError: when value cannot be converted to distance.

    """
    if __value is None:
        return float(default)

    if isinstance(__value, (float, int)):
        return float(__value)

    if isinstance(__value, str):
        return _from_string(__value, default)

    raise ValueError(f"{type(__value)} cannot be converted to distance")


def _from_string(__value: str, /, default: float) -> float:
    """Convert string to distance.

    Args:
        value: String representation of distance value.
        default: Default value.

    Returns:
        Amount.

    Raises:
        TypeError: when value is not type 'str'.
        ValueError: when value cannot be converted to distance.

    """
    if not isinstance(__value, str):
        message = f"expected type 'str', got {type(__value)} instead"
        raise TypeError(message)

    value = __value.replace("  ", " ").strip()
    if not value:
        return default

    try:
        pattern = r"(\d+),?(\d*.?\d*)\s?m?"
        replacement = r"\1\2"
        result = float(re.sub(pattern, replacement, value, flags=re.I))
    except ValueError:
        raise ValueError(f"{type(__value)} cannot be converted to distance")
    else:
        return result
