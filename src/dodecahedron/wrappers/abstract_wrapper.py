# -*- coding: utf-8 -*-
"""Abstract Wrapper."""

# pylint: disable=too-few-public-methods

# Standard Library Imports
import abc
from typing import Any


__all__ = ["AbstractWrapper"]


class AbstractWrapper(abc.ABC):
    """Represents an abstract wrapper."""

    @abc.abstractmethod
    def read(self, *args, **kwargs) -> Any:
        """Read data."""
        raise NotImplementedError

    @abc.abstractmethod
    def write(self, *args, **kwargs) -> None:
        """Write data."""
        raise NotImplementedError
