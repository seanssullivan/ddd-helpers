# -*- coding: utf-8 -*-
"""Message Broker."""

# Standard Library Imports
from __future__ import annotations
import abc
from collections import defaultdict
from datetime import datetime
import logging
from typing import Callable
from typing import Dict
from typing import List
from typing import Type


# Initialize logger.
log = logging.getLogger(__name__)


class AbstractMessageBroker(abc.ABC):
    """Represents an abstract message broker."""

    subscribers: Dict[str, List[Callable]]

    @abc.abstractmethod
    def publish(self, channel: str, event: str) -> None:
        """Publish an event to a channel.

        Args:
            channel: Name of channel.
            event: JSON representation of an event.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def subscribe(self, channel: str, subscriber: Callable) -> None:
        """Add subscriber to channel.

        Args:
            channel: Name of channel to which to subscribe.
            subscriber: Function to call for events on channel.

        """
        raise NotImplementedError


class MessageBroker(AbstractMessageBroker):
    """Implementation of a message broker."""

    _instance = None
    subscribers = defaultdict(list)

    def __new__(cls: Type[MessageBroker], *args, **kwargs) -> MessageBroker:
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)

        return cls._instance

    def publish(self, channel: str, event: str) -> None:
        """Publish an event to a channel.

        Args:
            channel: Name of channel.
            event: JSON representation of an event.

        """
        message = self.make_message(event)
        self.send_message(channel, message)

    @staticmethod
    def make_message(event: str, /) -> dict:
        """Make message to send to subscribers.

        Args:
            event: Published event.

        Returns:
            Message.

        """
        message = {"data": event, "created_at": datetime.now().isoformat()}
        return message

    def send_message(
        self, channel: str, message: Dict[str, str]
    ) -> None:  # pylint: disable=broad-except
        """Send message to channel subscribers.

        Args:
            channel: Name of channel.
            message: Message to send to subscribers.

        """
        for subscriber in self.subscribers[channel]:
            try:
                log.debug(
                    "sending %s event to subscriber %s", channel, subscriber
                )
                subscriber(message)
            except Exception:
                log.exception("Exception handling %s event", channel)
                continue

    def subscribe(self, channel: str, subscriber: Callable) -> None:
        """Add subscribe to channel.

        Args:
            channel: Name of channel to which to subscribe.
            subscriber: Function to call for events on channel.

        """
        self.subscribers[channel].append(subscriber)
