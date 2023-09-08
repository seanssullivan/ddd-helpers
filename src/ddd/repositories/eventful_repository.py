# -*- coding: utf-8 -*-
"""Eventful Repository.

Implementation based on 'Architecture Patterns in Python' repository pattern.

.. _Architecture Patterns in Python:
    https://github.com/cosmicpython/code

"""

# Standard Library Imports
import abc
from typing import Generator

# Local Imports
from .tracking_repository import AbstractTrackingRepository
from .tracking_repository import TrackingRepository
from ..messages import AbstractEvent
from ..messages import BaseEvent
from ..queue import MessageQueue

__all__ = [
    "AbstractEventfulRepository",
    "EventfulRepository",
]


class AbstractEventfulRepository(AbstractTrackingRepository):
    """Represents an abstract eventful repository."""

    @property
    @abc.abstractmethod
    def events(self) -> MessageQueue:
        """Events."""
        raise NotImplementedError

    @abc.abstractmethod
    def collect_events(self) -> Generator[AbstractEvent, None, None]:
        """Collect events."""
        raise NotImplementedError


class EventfulRepository(TrackingRepository, AbstractEventfulRepository):
    """Implements an eventful repository.

    Attributes:
        events: Events.

    """

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
