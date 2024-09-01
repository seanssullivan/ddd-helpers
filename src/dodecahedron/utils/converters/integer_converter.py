# -*- coding: utf-8 -*-
"""Integer Converter.

Module provides function for converting values to integers.

"""

__all__ = ["to_integer"]


def to_integer(__value: object, /, default: int = 0) -> int:
    """Convert value to integer.

    Args:
        __value: Value to convert to integer.
        default (optional): Default value. Default ``0``.

    Returns:
        Integer.

    Raises:
        ValueError: when value cannot be converted to integer.

    """
    if __value is None:
        return default

    if isinstance(__value, (float, int)):
        return int(__value)

    if isinstance(__value, str):
        return _from_string(__value, default)

    raise ValueError(f"{__value} cannot be converted to integer")


def _from_string(__value: str, /, default: int) -> int:
    """Convert string to integer.

    Args:
        value: String representation of integer value.
        default: Default value.

    Returns:
        Integer.

    Raises:
        TypeError: when value is not type 'str'.
        ValueError: when value cannot be converted to integer.

    """
    if not isinstance(__value, str):
        message = f"expected type 'str', got {type(__value)} instead"
        raise TypeError(message)

    value = __value.replace("  ", " ").strip()
    if not value:
        return default

    try:
        result = int(float(value))
    except ValueError:
        raise ValueError(f"{__value} cannot be converted to integer")
    else:
        return result
