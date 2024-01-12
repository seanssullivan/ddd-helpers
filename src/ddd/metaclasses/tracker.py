# -*- coding: utf-8 -*-

# Standard Library Imports
import abc
from types import MethodType
from typing import Any
from typing import Callable
from typing import TypeVar

# Local Imports
from .. import decorators
from ..decorators.tracking import SEEN_ATTR

__all__ = ["TrackerMeta"]


# Constants
ADD_METHOD = "add"
GET_METHOD = "get"
LIST_METHOD = "list"
REMOVE_METHOD = "remove"


# Custom types
T = TypeVar("T", bound=MethodType)


class TrackerMeta(abc.ABCMeta):
    """Metaclass for tracking child objects."""

    def __new__(meta, name: str, bases, attrs: dict) -> type:
        wrapped_attrs = meta.wrap_attributes(attrs)
        return super().__new__(meta, name, bases, wrapped_attrs)

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        instance = super().__call__(*args, **kwargs)
        setattr(instance, SEEN_ATTR, set())
        return instance

    @classmethod
    def wrap_attributes(cls, attrs: dict) -> dict:
        """Wrap attributes.

         Args:
            attrs: Attributes to wrap.

        Returns:
            Wrapped attributes.

        """
        results = {
            key: (
                cls.wrap_method(key, value)
                if isinstance(value, MethodType)
                else value
            )
            for key, value in attrs.items()
        }
        return results

    @classmethod
    def wrap_method(cls, name: str, method: Any) -> Callable:
        """Wrap method.

        Args:
            method: Method to wrap.

        Returns:
            Wrapped method.

        """
        if not isinstance(method, MethodType):
            message = f"expected method, got type {type(method)} instead"
            raise TypeError(message)

        if name == ADD_METHOD:
            return decorators.track_first_positional_argument(method)

        if name == GET_METHOD:
            return decorators.track_single_return_value(method)

        if name == LIST_METHOD:
            return decorators.track_multiple_return_values(method)

        if name == REMOVE_METHOD:
            return decorators.track_first_positional_argument(method)

        return method
