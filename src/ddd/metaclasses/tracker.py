# -*- coding: utf-8 -*-

# Standard Library Imports
import abc
import functools
from types import FunctionType
from typing import List
from typing import Union

__all__ = ["TrackerMeta"]


# Constants
ADD_METHOD = "add"
GET_METHOD = "get"
LIST_METHOD = "list"
REMOVE_METHOD = "remove"


class TrackerMeta(abc.ABCMeta):
    """Metaclass for tracking child objects."""

    def __new__(meta, name: str, bases, attrs: dict) -> type:
        wrapped_attrs = meta.wrap_attributes(attrs)
        return super().__new__(meta, name, bases, wrapped_attrs)

    def __call__(cls, *args, **kwargs) -> object:
        instance = super().__call__(*args, **kwargs)
        setattr(instance, "__seen__", set())
        return instance

    @classmethod
    def wrap_attributes(cls, attrs: dict) -> dict:
        """Wrap attributes.

         Args:
            attrs: Attributes to wrap.

        Returns:
            Wrapped attributes.

        """
        result = {
            key: (
                cls.wrap_method(key, value)
                if isinstance(value, FunctionType)
                else value
            )
            for key, value in attrs.items()
        }
        return result

    @classmethod
    def wrap_method(cls, name: str, method: FunctionType) -> FunctionType:
        """Wrap method.

        Args:
            method: Method to wrap.

        Returns:
            Wrapped method.

        """
        if not isinstance(method, FunctionType):
            message = f"expected function, got type {type(method)} instead"
            raise TypeError(message)

        if name == ADD_METHOD:
            return cls.wrap_add_method(method)

        if name == GET_METHOD:
            return cls.wrap_get_method(method)

        if name == LIST_METHOD:
            return cls.wrap_list_method(method)

        if name == REMOVE_METHOD:
            return cls.wrap_remove_method(method)

        return method

    @staticmethod
    def wrap_add_method(method: FunctionType) -> FunctionType:
        """Wrap `add` method.

        Args:
            method: Method to wrap.

        Returns:
            Wrapped method.

        """

        @functools.wraps(method)
        def wrapper(self: object, obj: object) -> None:
            method(self, obj)

            seen = getattr(self, "__seen__")  # type: set
            seen.add(obj)

        functools.update_wrapper(wrapper, method)
        return wrapper

    @staticmethod
    def wrap_get_method(method: FunctionType) -> FunctionType:
        """Wrap `get` method.

        Args:
            method: Method to wrap.

        Returns:
            Wrapped method.

        """

        @functools.wraps(method)
        def wrapper(self: object, ref: Union[int, str]) -> object:
            result = method(self, ref)

            seen = getattr(self, "__seen__")  # type: set
            seen.add(result)

            return result

        functools.update_wrapper(wrapper, method)
        return wrapper

    @staticmethod
    def wrap_list_method(method: FunctionType) -> FunctionType:
        """Wrap `list` method.

        Args:
            method: Method to wrap.

        Returns:
            Wrapped method.

        """

        @functools.wraps(method)
        def wrapper(self: object) -> List[object]:
            results = method(self)

            seen = getattr(self, "__seen__")  # type: set
            seen.update(results)

            return results

        functools.update_wrapper(wrapper, method)
        return wrapper

    @staticmethod
    def wrap_remove_method(method: FunctionType) -> FunctionType:
        """Wrap `remove` method.

        Args:
            method: Method to wrap.

        Returns:
            Wrapped method.

        """

        @functools.wraps(method)
        def wrapper(self: object, obj: object) -> None:
            method(self, obj)

            seen = getattr(self, "__seen__")  # type: set
            seen.discard(obj)

        functools.update_wrapper(wrapper, method)
        return wrapper
