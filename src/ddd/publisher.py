# -*- coding: utf-8 -*-

# Standard Imports
import abc
from dataclasses import asdict
import logging
import json
from operator import methodcaller

# Local Imports
from .messages import event

__all__ = [
    "AbstractPublisher",
    "BasePublisher",
]


# Initialize logger.
log = logging.getLogger(__name__)


class AbstractPublisher(abc.ABC):
    """Represents an abstract publisher."""

    @property
    @abc.abstractmethod
    def connection(self) -> object:
        """Connection."""
        raise NotImplementedError

    @abc.abstractmethod
    def publish(self, channel: str, event: event.BaseEvent, /) -> None:
        """Publish event to channel."""
        raise NotImplementedError


class BasePublisher(AbstractPublisher):
    """Implements a base class for publishers to inherit."""

    def publish(self, channel: str, event: event.BaseEvent, /) -> None:
        """publishes an event to an external message broker.

        Args:
            channel: Channel on which to publish event.
            event: Event to publish on external broker.

        """
        log.info("publishing: channel=%s, event=%s", channel, event)
        payload = json.dumps(asdict(event))

        methodcaller("publish", channel, payload)(self.connection)
