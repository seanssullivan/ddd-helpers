# -*- coding: utf-8 -*-
"""Boolean Converter.

Module provides function for converting values to booleans.

"""

__all__ = ["to_boolean"]


# Constants
FALSY_VALUES = ("false", "no", "n", "0")
TRUTHY_VALUES = ("true", "yes", "y", "1")


def to_boolean(__value: object, /, default: bool = False) -> bool:
    """Convert value to boolean.

    Args:
        __value: Value to convert to boolean.
        default (optional): Default value. Default ``False``.

    Returns:
        Boolean.

    Raises:
        ValueError: when value cannot be converted to boolean.

    """
    if __value is None:
        return default

    if isinstance(__value, bool):
        return __value

    if isinstance(__value, (float, int)):
        return bool(__value)

    if isinstance(__value, str):
        return _from_string(__value, default)

    raise ValueError(f"{__value} cannot be converted to boolean")


def _from_string(__value: str, /, default: bool) -> bool:
    """Convert string to boolean.

    Args:
        __value: String representation of boolean value.
        default: Default value.

    Returns:
        Boolean.

    Raises:
        ValueError: when value cannot be converted to boolean.

    """
    value = __value.replace("  ", "").strip()
    if not value:
        return default

    if value.lower() in TRUTHY_VALUES:
        return True

    if value.lower() in FALSY_VALUES:
        return False

    raise ValueError(f"{__value} cannot be converted to boolean")
