# -*- coding: utf-8 -*-
"""Events.

This module defines event classes. Events are simple data structures that work as
messages in the system, transmitting instructions from one part of the system to another.
Events distribute information whenever a specific event occurs so that subsequent actions
can be performed by processes in the system which are dependent on that information.
Events are always named using past-tense verb phrases.

"""

# Standard Library Imports
from dataclasses import dataclass

# Local Imports
from .message import AbstractMessage
from .message import BaseMessage

__all__ = [
    "AbstractEvent",
    "BaseEvent",
]


class AbstractEvent(AbstractMessage):
    """Represents an abstract event."""


@dataclass
class BaseEvent(BaseMessage, AbstractEvent):
    """Base class for events."""
