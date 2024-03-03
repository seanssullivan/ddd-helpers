# -*- coding: utf-8 -*-
"""Sessioned Unit of Work.

Based on 'Architecture Patterns in Python' unit-of-work pattern.

.. _Architecture Patterns in Python:
    https://github.com/cosmicpython/code

"""

# Standard Library Imports
from __future__ import annotations
from typing import Any
from typing import Callable
from typing import Optional
from typing import TypeVar

# Local Imports
from .base_unit_of_work import BaseUnitOfWork


# Custom types
T = TypeVar("T")

# Private attributes
SESSION_ATTR = "_session"


class SessionedUnitOfWork(BaseUnitOfWork):
    """Class implements a sessioned unit of work.

    Args:
        *args (optional): Positional arguments.
        session_factory (optional): Function for creating a session.
        **kwargs (optional): Keyword arguments.

    Attributes:
        session: Session.

    """

    def __init__(self, *args, session_factory: Callable, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._session_factory = session_factory

    @property
    def session(self) -> Optional[Any]:
        """Session."""
        return getattr(self, SESSION_ATTR, None)

    def __enter__(self) -> SessionedUnitOfWork:
        setattr(self, SESSION_ATTR, self._session_factory())
        super().__enter__()
        return self

    def __exit__(self, *args) -> None:
        super().__exit__(*args)
        self.close()

    def close(self) -> None:
        """Close session."""
        getattr(self.session, "close")()

    def commit(self) -> None:
        """Commit changes to repository."""
        getattr(self.session, "commit")()

    def rollback(self) -> None:
        """Rollback changes to repository."""
        getattr(self.session, "rollback")()
