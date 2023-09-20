# -*- coding: utf-8 -*-
"""Abstract Unit of Work.

Based on 'Architecture Patterns in Python' unit-of-work pattern.

.. _Architecture Patterns in Python:
    https://github.com/cosmicpython/code

"""

# Standard Library Imports
from __future__ import annotations
import abc

__all__ = ["AbstractUnitOfWork"]


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
