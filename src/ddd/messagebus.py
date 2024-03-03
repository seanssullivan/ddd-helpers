# -*- coding: utf-8 -*-
"""Message Bus.

This module defines message-bus classes which delivers commands and events
to their respective handlers.

Commands are simple data structures that capture an intent for the system to
perform a particular action: commands are always matched to a single handler.
When a command is executed, there is an expectation that an event will occur
as a result; whenever a process fails, the process or user that created the
command must receive an error message containing pertinent information.

Events are data structures that are broadcast to all subscribed listeners.
Events are never assigned to dedicated event handlers. Instead, handlers are
registered with the message bus and wait for an event to occur before
performing a particular action. Events reflect business logic described in
terms of 'if this happens, then do that'. They are used to implement workflows
in the system.

Implementation based on 'Architecture Patterns in Python' message-bus pattern.

.. _Architecture Patterns in Python:
    https://github.com/cosmicpython/code

"""

# Standard Library Imports
from __future__ import annotations
import abc
import logging
from operator import methodcaller
from typing import Callable
from typing import Dict
from typing import List
from typing import Type

# Local Imports
from .errors import BaseError
from .messages import AbstractMessage
from .messages import AbstractCommand
from .messages import AbstractEvent
from .queue import MessageQueue
from .units_of_work import AbstractUnitOfWork

__all__ = ["AbstractMessageBus"]


# Initialize logger.
log = logging.getLogger(__name__)

# Constants
eventcollector = methodcaller("collect_events")


class AbstractMessageBus(abc.ABC):
    """Represents an abstract message bus.

    Attributes:
        uow: Unit of work.
        queue: Message queue.

    """

    uow: AbstractUnitOfWork
    queue: MessageQueue[AbstractMessage]

    @abc.abstractmethod
    def handle(self, message: AbstractMessage) -> None:
        """Handle a message.

        Args:
            message: Message to handle.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def subscribe(
        self, message: Type[AbstractMessage], handler: Callable
    ) -> None:
        """Subscribe a handler for a `Command` or `Event`.

        Args:
            message: Message type to which to subscribe.

        """
        raise NotImplementedError


class BaseMessageBus(AbstractMessageBus):
    """Implements a base class for message buses to inherit.

    Args:
        uow: Unit of work.
        command_handlers: Dictionary of commands and handlers.
            Each command is associated with a single handler.
        event_handlers: Dictionary of events and handlers.
            Each event is associated with multiple handlers.

    Attributes:
        uow: Unit of work.
        queue: Message queue.

    """

    queue: MessageQueue

    def __init__(
        self,
        uow: AbstractUnitOfWork,
        command_handlers: Dict[Type[AbstractCommand], Callable],
        event_handlers: Dict[Type[AbstractEvent], List[Callable]],
    ) -> None:
        self.uow = uow
        self.command_handlers = command_handlers
        self.event_handlers = event_handlers

    def handle(self, message: AbstractMessage) -> None:
        """Handle a message.

        Provided message is passed to an appropriate handler function.

        Args:
            message: Message.

        """
        self.queue = MessageQueue([message])
        while self.queue:
            message = self.queue.popleft()
            self.handle_message(message)

    def subscribe(
        self, message: Type[AbstractMessage], handler: Callable
    ) -> None:
        """Subscribe a handler for a `Command` or `Event`.

        Args:
            message: Message type to which to subscribe.
            handler: Handler function to subscribe.

        """
        if issubclass(message, AbstractCommand):
            self.command_handlers[message] = handler
        elif issubclass(message, AbstractEvent):
            self.event_handlers[message].append(handler)
        else:
            error = f"{type(message)} is not a 'Command' or an 'Event'"
            raise TypeError(error)

    def handle_message(self, message: AbstractMessage) -> None:
        """Handle message.

        Args:
            message: Message to handle.

        """
        if isinstance(message, AbstractCommand):
            self.handle_command(message)
        elif isinstance(message, AbstractEvent):
            self.handle_event(message)
        else:
            error = f"{message} was not a 'Command' or an 'Event'"
            raise TypeError(error)

    def handle_command(self, command: AbstractCommand) -> None:
        """Handle command.

        Args:
            command: Command to handle.

        """
        try:
            handler = self.command_handlers[type(command)]
            handler(command)
        except BaseError as error:
            log.exception("Error handling command %s", command)
            raise error
        else:
            self.collect_events()

    def handle_event(self, event: AbstractEvent) -> None:
        """Handle event.

        Args:
            event: Event to handle.

        """
        for handler in self.event_handlers[type(event)]:
            try:
                log.debug("handling event %s with handler %s", event, handler)
                handler(event)
            except BaseError:
                log.exception("Error handling event %s", event)
                continue
            else:
                self.collect_events()

    def collect_events(self) -> None:
        """Collect events."""
        if hasattr(self.uow, "collect_events"):
            events = list(eventcollector(self.uow))
            self.queue.extend(events)
