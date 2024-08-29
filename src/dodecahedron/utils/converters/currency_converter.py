# -*- coding: utf-8 -*-
"""Currency Converter.

Module provides function for converting values to currencies.

"""

# Standard Library Imports
import re

__all__ = ["to_currency"]


def to_currency(__value: object, /, default: float = 0) -> float:
    """Convert value to currency.

    Args:
        __value: Value to convert to currency.
        default (optional): Default value. Default ``0``.

    Returns:
        Amount.

    Raises:
        ValueError: when value cannot be converted to float.

    """
    if __value is None:
        return float(default)

    if isinstance(__value, (float, int)):
        return round(float(__value), 2)

    if isinstance(__value, str):
        return _from_string(__value, default)

    raise ValueError(f"{__value} cannot be converted to currency")


def _from_string(__value: str, /, default: float) -> float:
    """Convert string to currency.

    Args:
        __value: String representation of currency value.
        default: Default value.

    Returns:
        Amount.

    Raises:
        TypeError: when value is not type 'str'.
        ValueError: when value cannot be converted to float.

    """
    if not isinstance(__value, str):
        message = f"expected type 'str', got {type(__value)} instead"
        raise TypeError(message)

    value = __value.replace("  ", "").strip()
    if not value:
        return default

    try:
        amount = float(re.sub(r"(\d+),(\d+.?\d*)", r"\1\2", value))
    except ValueError:
        raise ValueError(f"{__value} cannot be converted to currency")
    else:
        return round(amount, 2)
