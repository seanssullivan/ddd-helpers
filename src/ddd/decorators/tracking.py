# -*- coding: utf-8 -*-

# Standard Library Imports
import functools
from types import MethodType
from typing import Any
from typing import Sequence

__all__ = [
    "track_first_positional_argument",
    "track_multiple_return_values",
    "track_single_return_value",
]

# Constants
SEEN_ATTR = "__seen__"


def track_first_positional_argument(method: MethodType, /) -> MethodType:
    """Track first positional argument passed to method.

    Args:
        method: Method to track.

    Returns:
        Wrapped function.

    """

    @functools.wraps(method)
    def wrapper(self, obj: object, /, *args, **kwargs) -> Any:
        """Wrapper applied to decorated method.

        Args:
            obj: Object to track.
            *args: Positional arguments to pass to wrapped method.
            **kwargs: Keyword arguments to pass to wrapped method.

        Returns:
            Result of called method.

        """
        result = method(self, obj, *args, **kwargs)

        # We only add objects to those seen after the method executes
        # successfully. We don't want to track objects that raise exceptions.
        add_seen_object(self, obj)
        return result

    functools.update_wrapper(wrapper, method)
    return wrapper


def track_multiple_return_values(method: MethodType, /) -> MethodType:
    """Track all values returned from method.

    Args:
        method: Method to track.

    Returns:
        Wrapped function.

    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs) -> Sequence:
        """Wrapper applied to decorated method.

        Args:
            *args: Positional arguments to pass to wrapped method.
            **kwargs: Keyword arguments to pass to wrapped method.

        Returns:
            Results of called method.

        """
        results = method(self, *args, **kwargs)
        if results is not None:
            update_seen_objects(self, results)

        return results

    functools.update_wrapper(wrapper, method)
    return wrapper


def track_single_return_value(method: MethodType, /) -> MethodType:
    """Track each value returned from method.

    Args:
        method: Method to track.

    Returns:
        Wrapped function.

    """

    @functools.wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """Wrapper applied to decorated method.

        Args:
            *args: Positional arguments to pass to wrapped method.
            **kwargs: Keyword arguments to pass to wrapped method.

        Returns:
            Result of called method.

        """
        result = method(self, *args, **kwargs)
        if result is not None:
            add_seen_object(self, result)

        return result

    functools.update_wrapper(wrapper, method)
    return wrapper


# ----------------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------------
def add_seen_object(parent: Any, child: Any) -> None:
    """Add value to seen objects.

    Args:
        parent: Parent object.
        child: Child object seen.

    """
    set_default_attr(parent, SEEN_ATTR, set())
    seen = getattr(parent, SEEN_ATTR)  # type: set
    seen.add(child)


def update_seen_objects(parent: Any, children: Sequence) -> None:
    """Add results to seen objects.

    Args:
        parent: Parent object.
        children: Child objects seen.

    """
    set_default_attr(parent, SEEN_ATTR, set())
    seen = getattr(parent, SEEN_ATTR)  # type: set
    seen.update(children)


def set_default_attr(obj: object, attr: str, value: Any) -> None:
    """Set default value of attribute on object.

    Args:
        obj: Object on which to set default attribute.
        attr: Name of attribute to set.
        value: Value to which to set attribute.

    """
    if not hasattr(obj, attr):
        setattr(obj, attr, value)
