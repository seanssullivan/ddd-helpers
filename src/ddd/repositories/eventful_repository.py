# -*- coding: utf-8 -*-
"""Eventful Repository.

Implementation based on 'Architecture Patterns in Python' repository pattern.

.. _Architecture Patterns in Python:
    https://github.com/cosmicpython/code

"""

# Standard Library Imports
from typing import Deque
from typing import Generator
from typing import Iterable
from typing import List

# Local Imports
from .abstract_repository import AbstractRepository
from ..messages import AbstractEvent
from ..metaclasses import SingletonMeta
from ..metaclasses import TrackerMeta
from ..queue import MessageQueue

__all__ = ["EventfulRepository"]


class RepositoryMeta(SingletonMeta, TrackerMeta):
    """Implements a repository metaclass.

    Combines the singleton and tracker metaclasses into a single metaclass
    for use by repositories.

    """


class EventfulRepository(AbstractRepository, metaclass=RepositoryMeta):
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

    def collect_events(self) -> Generator[AbstractEvent, None, None]:
        """Collect events.

        Yields:
            Events.

        """
        self._update_events()
        while self.events:
            yield self.events.popleft()

    def _update_events(self) -> None:
        """Update events."""
        events = self._get_child_events()
        self.events.extend(events)
        self.events.sort()

    def _get_child_events(self) -> List[AbstractEvent]:
        """Get events from child objects.

        Returns:
            Events.

        """
        seen = getattr(self, "__seen__")  # type: set
        results = collect_events_from_objects(seen)
        # seen.clear()
        return results


def collect_events_from_objects(objs: Iterable) -> List[AbstractEvent]:
    """Collect events from objects.

    Args:
        objs: Objects from which to collect events.

    Returns:
        Events.

    """
    results = []
    for obj in objs:
        events = collect_events_from_object(obj)
        results.extend(events)

    return results


def collect_events_from_object(obj: object) -> List[AbstractEvent]:
    """Collect events from object.

    Args:
        obj: Object from which to collect events.

    Returns:
        Events.

    """
    results = []
    while getattr(obj, "events", None):
        events = getattr(obj, "events")  # type: Deque[AbstractEvent]
        event = events.popleft()  # type: AbstractEvent
        results.append(event)

    return results
