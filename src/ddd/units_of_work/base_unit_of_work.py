# -*- coding: utf-8 -*-
"""Base Unit of Work."""

# Standard Library Imports
from __future__ import annotations
from typing import Optional
from typing import Type

# Local Imports
from .abstract_unit_of_work import AbstractUnitOfWork

__all__ = ["BaseUnitOfWork"]


# Constants
AUTO_COMMIT_ATTR = "_auto_commit"


class BaseUnitOfWork(AbstractUnitOfWork):
    """Implements a base class for units of work to inherit.

    Attributes:
        auto_commit: Whether to auto commit.

    """

    def __enter__(self) -> BaseUnitOfWork:
        return self

    def __exit__(self, exc: Optional[Type[Exception]], *_) -> None:
        if self.auto_commit is True and not exc:
            self.commit()

    @property
    def auto_commit(self) -> bool:
        """Whether to auto commit.

        Raises:
            TypeError: when value is not type 'bool'.

        """
        result = getattr(self, AUTO_COMMIT_ATTR, False)
        return result

    @auto_commit.setter
    def auto_commit(self, value: bool) -> None:
        if not isinstance(value, bool):
            message = f"expected type 'bool', got {type(value)} instead"
            raise TypeError(message)

        setattr(self, AUTO_COMMIT_ATTR, value)

    def commit(self) -> None:
        """Commit changes."""

    def rollback(self) -> None:
        """Rollback changes."""
