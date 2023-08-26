# -*- coding: utf-8 -*-
"""Abstract Repository.

Implementation based on 'Architecture Patterns in Python' repository pattern.

.. _Architecture Patterns in Python:
    https://github.com/cosmicpython/code

"""

# Standard Library Imports
import abc
import functools
from types import FunctionType
from typing import Deque
from typing import Generator
from typing import List
from typing import Set
from typing import Union

# Local Imports
from .models import AbstractAggregate
from .messages import AbstractEvent
from .messages import BaseEvent
from .queue import MessageQueue

__all__ = [
    "AbstractRepository",
    "AbstractTrackingRepository",
    "AbstractEventfulRepository",
    "EventfulRepository",
]


# Constants
ADD_METHOD = "add"
GET_METHOD = "get"
LIST_METHOD = "list"
REMOVE_METHOD = "remove"


class AbstractRepository(abc.ABC):
    """Represents an abstract repository."""

    @abc.abstractmethod
    def add(self, obj: object) -> None:
        """Add object to repository.

        Args:
            obj: Object to add to repository.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, ref: Union[int, str]) -> object:
        """Get object from repository.

        Args:
            ref: Reference to object.

        Returns:
            Object.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[object]:
        """List objects in repository.

        Returns:
            Objects in repository.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, obj: object) -> None:
        """Remove object from repository.

        Args:
            obj: Object to remove from repository.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def close(self) -> None:
        """Close connection to repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def commit(self) -> None:
        """Commit changes to repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self) -> None:
        """Rollback changes to repository."""
        raise NotImplementedError


class Tracker(abc.ABCMeta):
    """Metaclass for tracking child objects."""

    def __new__(meta, name: str, bases, attrs: dict) -> type:
        wrapped_attrs = meta.wrap_attributes(attrs)
        return super().__new__(meta, name, bases, wrapped_attrs)

    def __call__(cls, *args, **kwargs) -> AbstractRepository:
        instance = super().__call__(*args, **kwargs)
        setattr(instance, "seen", set())
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

    seen: Set[AbstractAggregate]


class AbstractEventfulRepository(AbstractTrackingRepository):
    """Represents an abstract eventful repository."""

    @property
    @abc.abstractmethod
    def events(self) -> Deque[AbstractEvent]:
        """Events."""
        raise NotImplementedError

    @abc.abstractmethod
    def collect_events(self) -> Generator[AbstractEvent, None, None]:
        """Collect events."""
        raise NotImplementedError


class EventfulRepository(AbstractEventfulRepository):
    """Implements an eventful repository."""

    def __init__(self) -> None:
        super().__init__()
        self._events = MessageQueue()

    @property
    def events(self) -> MessageQueue:
        """Events."""
        return self._events

    def collect_events(self) -> Generator[BaseEvent, None, None]:
        """Collect events.

        Yields:
            Events.

        """
        self._collect_child_events()
        while self.events:
            yield self.events.popleft()

    def _collect_child_events(self) -> None:
        """Collect events from child objects."""
        for obj in self.seen:
            while getattr(obj, "events", None):
                event = obj.events.popleft()
                self.events.append(event)

        self.events.sort()
