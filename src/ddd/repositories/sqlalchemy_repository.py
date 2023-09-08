# -*- coding: utf-8 -*-

# Standard Library Imports
import abc
from typing import TYPE_CHECKING

# Local Imports
from .abstract_repository import AbstractRepository

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

__all__ = [
    "AbstractSqlAlchemyRepository",
    "SqlAlchemyRepository",
]


class AbstractSqlAlchemyRepository(AbstractRepository):
    """Represents an abstract SQLAlchemy repository."""

    @property
    @abc.abstractmethod
    def session(self) -> "Session":
        """SQLAlchemy session."""
        raise NotImplementedError

    @abc.abstractmethod
    def close(self) -> None:
        """Close connection to repository."""
        raise NotImplementedError


class SqlAlchemyRepository(AbstractSqlAlchemyRepository):
    """Implements an SQLAlchemy repository.

    The repository uses SQLAlchemy to read data from a database and to handle
    relevant CRUD operations.

    Attributes:
        session: SQLAlchemy session.

    .. _SQLAlchemy Documentation:
        https://docs.sqlalchemy.org/

    """

    def __init__(self, session: "Session", /, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._session = session

    @property
    def session(self) -> "Session":
        """SQLAlchemy session."""
        return self._session

    def close(self) -> None:
        """Close connection to repository."""
        self.session.close()

    def commit(self) -> None:
        """Commit changes to repository."""
        self.session.commit()

    def rollback(self) -> None:
        """Rollback changes to repository."""
        self.session.rollback()
