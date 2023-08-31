# -*- coding: utf-8 -*-
"""Tracking Repository.

Implementation based on 'Architecture Patterns in Python' repository pattern.

.. _Architecture Patterns in Python:
    https://github.com/cosmicpython/code

"""

# Standard Library Imports
import abc
import functools
from types import FunctionType
from typing import List
from typing import Set
from typing import Union

# Local Imports
from ..models import AbstractAggregate
from .abstract_repository import AbstractRepository

__all__ = [
    "AbstractTrackingRepository",
    "TrackingRepository",
]


# Constants
ADD_METHOD = "add"
GET_METHOD = "get"
LIST_METHOD = "list"
REMOVE_METHOD = "remove"


class Tracker(abc.ABCMeta):
    """Metaclass for tracking child objects."""

    def __new__(meta, name: str, bases, attrs: dict) -> type:
        wrapped_attrs = meta.wrap_attributes(attrs)
        return super().__new__(meta, name, bases, wrapped_attrs)

    def __call__(cls, *args, **kwargs) -> AbstractRepository:
        instance = super().__call__(*args, **kwargs)
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
        def wrapper(self: AbstractTrackingRepository, obj: object) -> None:
            method(self, obj)
            self.seen.add(obj)

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
        def wrapper(
            self: AbstractTrackingRepository, ref: Union[int, str]
        ) -> object:
            result = method(self, ref)
            self.seen.add(result)
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
        def wrapper(self: AbstractTrackingRepository) -> List[object]:
            results = method(self)
            self.seen.update(results)
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
        def wrapper(self: AbstractTrackingRepository, obj: object) -> None:
            method(self, obj)
            self.seen.discard(obj)

        functools.update_wrapper(wrapper, method)
        return wrapper


class AbstractTrackingRepository(AbstractRepository, metaclass=Tracker):
    """Represents an abstract tracking repository."""

    @property
    @abc.abstractmethod
    def seen(self) -> Set[AbstractAggregate]:
        """Objects seen."""
        raise NotImplementedError


class TrackingRepository(AbstractTrackingRepository):
    """Implements a tracking repository.

    Attributes:
        seen: Objects seen.

    """

    def __init__(self) -> None:
        super().__init__()
        self._seen = set()

    @property
    def seen(self) -> Set[AbstractAggregate]:
        """Objects seen."""
        return self._seen
