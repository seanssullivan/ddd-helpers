# -*- coding: utf-8 -*-
"""Message."""

# pylint: disable=too-few-public-methods

# Standard Library Imports
import abc
from dataclasses import dataclass
import datetime

__all__ = [
    "AbstractMessage",
    "BaseMessage",
]


class AbstractMessage(abc.ABC):
    """Represents an abstract message."""

    created_at: datetime.datetime

    def __gt__(self, other: object) -> bool:
        result = (
            self.created_at > other.created_at
            if isinstance(other, AbstractMessage)
            else False
        )
        return result

    def __lt__(self, other: object) -> bool:
        result = (
            self.created_at < other.created_at
            if isinstance(other, AbstractMessage)
            else False
        )
        return result


@dataclass
class BaseMessage(AbstractMessage):
    """Base class for messages."""

    def __post_init__(self) -> None:
        self.created_at = datetime.datetime.now()
