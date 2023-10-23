# -*- coding: utf-8 -*-

# Standard Library Imports
import functools
from types import FunctionType
from typing import Any


def track_argument(__method: FunctionType, /) -> FunctionType:
    """Track argument of method.

    Args:
        method: Method to track.

    Returns:
        Wrapped function.

    """

    @functools.wraps(__method)
    def wrapper(self, *args, **kwargs) -> Any:
        """Wrapper applied to decorated method.

        Args:
            self: Class of method.
            *args: Positional arguments to pass to wrapped method.
            **kwargs: Keyword arguments to pass to wrapped method.

        Returns:
            Result of called method.

        """
        set_default_attr(self, "__seen__", set())

        if args:
            raise_for_builtin(args[0])
            seen = getattr(self, "__seen__")  # type: set
            seen.add(args[0])

        result = __method(self, *args, **kwargs)
        return result

    functools.update_wrapper(wrapper, __method)
    return wrapper


def track_return(__method: FunctionType, /) -> FunctionType:
    """Track return value of method.

    Args:
        method: Method to track.

    Returns:
        Wrapped function.

    """

    @functools.wraps(__method)
    def wrapper(self, *args, **kwargs) -> Any:
        """Wrapper applied to decorated method.

        Args:
            self: Class of method.
            *args: Positional arguments to pass to wrapped method.
            **kwargs: Keyword arguments to pass to wrapped method.

        Returns:
            Result of called method.

        """
        set_default_attr(self, "__seen__", set())

        result = __method(self, *args, **kwargs)
        raise_for_builtin(result)

        if result is not None:
            seen = getattr(self, "__seen__")  # type: set
            seen.add(result)

        return result

    functools.update_wrapper(wrapper, __method)
    return wrapper


# ----------------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------------
def set_default_attr(obj: object, attr: str, value: Any) -> None:
    """Set default value of attribute on object.

    Args:
        obj: Object on which to set default attribute.
        attr: Name of attribute to set.
        value: Value to which to set attribute.

    """
    if not hasattr(obj, attr):
        setattr(obj, attr, value)


def raise_for_builtin(obj: object, /) -> None:
    """Raise error if object is instance of a builtin class.

    Args:
        obj: Object.

    Raises:
        TypeError: when argument is instance of a builtin class.

    """
    if is_builtin(obj):
        message = "argument is instance of builtin class"
        raise TypeError(": ".join([message, type(obj)]))


def is_builtin(obj: object, /) -> bool:
    """Check whether object is an instance of a builtin class.

    Args:
        obj: Object to check.

    Returns:
        Whether object is an instance of a builtin class.

    """
    result = obj.__class__.__module__ == "__builtins__"
    return result
