# -*- coding: utf-8 -*-
"""Yes or No Converter.

Module provides function for converting values to 'Yes' or 'No'.

"""

# Standard Library Imports
from typing import Literal
from typing import Optional
from typing import Union

__all__ = ["to_y_or_n", "to_yes_or_no"]


# Constants
FALSY_VALUES = ("false", "no", "n", "0")
TRUTHY_VALUES = ("true", "yes", "y", "1")


def to_y_or_n(
    __value: object, /, default: Optional[str] = None
) -> Optional[Literal["N", "Y"]]:
    """Convert value to `Y` or `N`.

    Args:
        value: Value to convert.
        default (optional): Default value. Default ``None``.

    Returns:
        `Y` or `N`.

    """
    if default and default not in ("Y", "N"):
        message = f"expected value of 'Y' or 'N', got {default} instead"
        raise ValueError(message)

    try:
        result = to_yes_or_no(__value)

    except TypeError:
        message = f"{type(__value)} cannot be converted to 'Y' or 'N'"
        raise ValueError(message)

    except ValueError:
        message = f"'{__value}' cannot be converted to 'Y' or 'N'"
        raise ValueError(message)

    return result[0] if result else default


def to_yes_or_no(
    __value: object, /, default: Optional[str] = None
) -> Optional[Literal["No", "Yes"]]:
    """Convert value to `Yes` or `No`.

    Args:
        value: Value to convert.
        default (optional): Default value. Default ``None``.

    Returns:
        `Yes` or `No`.

    """
    if default and default not in ("Yes", "No"):
        message = f"expected value of 'Yes' or 'No', got {default} instead"
        raise ValueError(message)

    if __value is None:
        return default

    if isinstance(__value, bool):
        return _from_boolean(__value)

    if isinstance(__value, (float, int)):
        return _from_integer(int(__value))

    if isinstance(__value, str):
        return _from_string(__value, default)

    raise TypeError(f"{type(__value)} cannot be converted to 'Yes' or 'No'")


def _from_boolean(__value: bool, /) -> Literal["No", "Yes"]:
    """Convert boolean to `Yes` or `No`.

    Args:
        __value: Value to convert to `Yes` or `No`.

    Returns:
        `Yes` or `No`.

    Raises:
        ValueError: when value cannot be converted to `Yes` or `No`.

    """
    result = "Yes" if __value is True else "No"
    return result


def _from_integer(__value: Union[float, int], /) -> Literal["No", "Yes"]:
    """Convert integer to `Yes` or `No`.

    Args:
        __value: Value to convert to `Yes` or `No`.

    Returns:
        `Yes` or `No`.

    Raises:
        ValueError: when value cannot be converted to `Yes` or `No`.

    """
    result = "Yes" if __value > 0 else "No"
    return result


def _from_string(
    __value: str, /, default: Optional[str] = None
) -> Optional[str]:
    """Convert string to `Yes` or `No`.

    Args:
        __value: String representation of `Yes` or `No`.
        default (optional): Default value. Default ``None``.

    Returns:
        `Yes` or `No`.

    Raises:
        ValueError: when value cannot be converted to `Yes` or `No`.

    """
    value = __value.replace("  ", " ").strip()
    if not value:
        return default

    if value.lower() in TRUTHY_VALUES:
        return "Yes"

    if value.lower() in FALSY_VALUES:
        return "No"

    raise ValueError(f"'{__value!s}' cannot be converted to 'Yes' or 'No'")
