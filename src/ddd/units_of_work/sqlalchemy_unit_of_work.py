# -*- coding: utf-8 -*-
"""SQLAlchemy Unit of Work.

Based on 'Architecture Patterns in Python' unit-of-work pattern.

.. _Architecture Patterns in Python:
    https://github.com/cosmicpython/code

"""

# Standard Library Imports
from __future__ import annotations
from typing import Callable
from typing import Optional
from typing import Type
from typing import TYPE_CHECKING

# Local Imports
from .eventful_unit_of_work import EventfulUnitOfWork

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


# Private attributes
SESSION_ATTR = "_session"


class SQLAlchemyUnitOfWork(EventfulUnitOfWork):
    """Class implements an SQLAlchemy unit of work.

    Args:
        session_factory (optional): Function for creating a database session.

    Attributes:
        session: Database session.

    """

    def __init__(self, session_factory: Callable[..., "Session"], /) -> None:
        super().__init__()
        self._session_factory = session_factory

    @property
    def session(self) -> Optional["Session"]:
        """SQLAlchemy session."""
        return getattr(self, SESSION_ATTR, None)

    def __enter__(self) -> SQLAlchemyUnitOfWork:
        setattr(self, SESSION_ATTR, self._session_factory())
        super().__enter__()
        return self

    def __exit__(self, *args) -> None:
        super().__exit__(*args)
        self.close()

    def close(self) -> None:
        """Close session."""
        self.session.close()

    def commit(self) -> None:
        """Commit changes to repository."""
        self.session.commit()

    def rollback(self) -> None:
        """Rollback changes to repository."""
        self.session.rollback()
