# -*- coding: utf-8 -*-
"""Abstract Repository.

Implementation based on 'Architecture Patterns in Python' repository pattern.

.. _Architecture Patterns in Python:
    https://github.com/cosmicpython/code

"""

# Standard Library Imports
import abc
from typing import List
from typing import Union

__all__ = ["AbstractRepository"]


class AbstractRepository(abc.ABC):
    """Represents an abstract repository."""

    @abc.abstractmethod
    def add(self, obj: object) -> None:
        """Add object to repository.

        Args:
            obj: Object to add to repository.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, ref: Union[int, str]) -> object:
        """Get object from repository.

        Args:
            ref: Reference to object.

        Returns:
            Object.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> List[object]:
        """List objects in repository.

        Returns:
            Objects in repository.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self, obj: object) -> None:
        """Remove object from repository.

        Args:
            obj: Object to remove from repository.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def commit(self) -> None:
        """Commit changes to repository."""
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self) -> None:
        """Rollback changes to repository."""
        raise NotImplementedError
