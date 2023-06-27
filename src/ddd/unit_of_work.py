# -*- coding: utf-8 -*-
"""Unit of Work.

Based on 'Architecture Patterns in Python' unit-of-work pattern.

.. _Architecture Patterns in Python:
    https://github.com/cosmicpython/code

"""

# Standard Library Imports
from __future__ import annotations
import abc
from typing import Generator

# Local Imports
from .messages import AbstractEvent
from .messages import BaseEvent
from .queue import AbstractQueue
from .queue import MessageQueue

__all__ = [
    "AbstractUnitOfWork",
    "BaseUnitOfWork",
    "AbstractEventfulUnitOfWork",
    "EventfulUnitOfWork",
]


class AbstractUnitOfWork(abc.ABC):
    """Represents an abstract unit of work."""

    @abc.abstractmethod
    def __enter__(self) -> AbstractUnitOfWork:
        raise NotImplementedError

    @abc.abstractmethod
    def __exit__(self, *_) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def commit(self) -> None:
        """Commit changes."""
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self) -> None:
        """Rollback changes."""
        raise NotImplementedError


class BaseUnitOfWork(AbstractUnitOfWork):
    """Implements a base Unit of Work."""

    def __enter__(self) -> BaseUnitOfWork:
        return self

    def __exit__(self, *_) -> None:
        pass

    def commit(self) -> None:
        """Commit changes."""
        pass

    def rollback(self) -> None:
        """Rollback changes."""
        pass


class AbstractEventfulUnitOfWork(AbstractUnitOfWork):
    """Represents an abstract eventful unit of work."""

    @property
    @abc.abstractmethod
    def events(self) -> AbstractQueue[AbstractEvent]:
        """Event queue."""
        raise NotImplementedError

    @abc.abstractmethod
    def collect_events(self) -> Generator[AbstractEvent, None, None]:
        """Collect events.

        Yields:
            Event.

        """
        raise NotImplementedError


class EventfulUnitOfWork(AbstractUnitOfWork):
    """Implements an eventful unit of work."""

    def __init__(self) -> None:
        super().__init__()
        self._events = MessageQueue()

    def __enter__(self) -> EventfulUnitOfWork:
        self._events.clear()
        return self

    def __exit__(self, *_) -> None:
        pass

    @property
    def events(self) -> MessageQueue:
        """Event queue."""
        return self._events

    def collect_events(self) -> Generator[BaseEvent, None, None]:
        """Collect events.

        Yields:
            Event.

        """
        while self.events:
            yield self.events.popleft()
