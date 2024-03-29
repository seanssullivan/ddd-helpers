# -*- coding: utf-8 -*-

# Standard Library Imports
import abc
from typing import Any
from typing import TYPE_CHECKING

# Local Imports
from .abstract_repository import AbstractRepository

if TYPE_CHECKING:
    from sqlalchemy.orm import Session  # type: ignore

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
    def execute(self, *args, **kwargs) -> Any:
        """Call the `execute` method directly on the SQLAlchemy session.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Results.

        """
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

    def execute(self, *args, **kwargs) -> Any:
        """Call the execute method directly on the SQLAlchemy session.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            Result.

        """
        result = self.session.execute(*args, **kwargs)
        return result

    def close(self) -> None:
        """Close connection to repository."""
        self.session.close()

    def commit(self) -> None:
        """Commit changes to repository."""
        self.session.commit()

    def rollback(self) -> None:
        """Rollback changes to repository."""
        self.session.rollback()
