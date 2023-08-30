# -*- coding: utf-8 -*-
"""Abstract models.

This module defines an abstract base class for models.

"""

# pylint: disable=too-few-public-methods

# Standard Library Imports
import abc
from typing import Deque

# Local Imports
from ..messages import AbstractEvent

__all__ = [
    "AbstractModel",
    "AbstractDispatcher",
    "AbstractAggregate",
]


class AbstractModel(abc.ABC):
    """Represents an abstract model."""

    @abc.abstractmethod
    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def __hash__(self) -> int:
        raise NotImplementedError


class AbstractDispatcher(abc.ABC):
    """Represents an abstract dispatcher.

    Dispatchers record events raised by the domain model.

    Attributes:
        events: Events raised by the domain model.

    """

    @property
    @abc.abstractmethod
    def events(self) -> Deque[AbstractEvent]:
        """Events."""
        raise NotImplementedError


class AbstractAggregate(AbstractModel, AbstractDispatcher):
    """Represents an abstract aggregate.

    The primary purpose of an aggregate is not simply to hold a collection of
    objects; instead, the purpose of an aggregate is to record events raised
    by the domain model. In addition, the aggregate encapsulates whatever
    business logic is involved when adding and removing objects.

    """

    @abc.abstractmethod
    def __contains__(self, obj: object) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def add(self, obj: object) -> None:
        """Add object to aggregate."""
        raise NotImplementedError

    @abc.abstractmethod
    def can_add(self, obj: object) -> bool:
        """Check whether object can be added to aggregate."""
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, ref: str) -> object:
        """Retrieve object from aggregate."""
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, obj: object) -> None:
        """Remove object from aggregate."""
        raise NotImplementedError
