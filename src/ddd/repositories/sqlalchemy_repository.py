# -*- coding: utf-8 -*-

# Standard Library Imports
import abc
import importlib
import operator
from typing import Any
from typing import TYPE_CHECKING

# Local Imports
from .abstract_repository import AbstractRepository

if TYPE_CHECKING:
    sqlalchemy = importlib.import_module("sqlalchemy")

__all__ = [
    "AbstractSqlAlchemyRepository",
    "SqlAlchemyRepository",
]


class AbstractSqlAlchemyRepository(AbstractRepository):
    """Represents an abstract SQLAlchemy repository."""

    @property
    @abc.abstractmethod
    def session(self) -> Any:
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

    def __init__(
        self, session: "sqlalchemy.orm.Session", /, *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self._session = session

    @property
    def session(self) -> "sqlalchemy.orm.Session":
        """SQLAlchemy session."""
        return self._session

    def close(self) -> None:
        """Close connection to repository."""
        operator.methodcaller("close")(self.session)

    def commit(self) -> None:
        """Commit changes to repository."""
        operator.methodcaller("commit")(self.session)

    def rollback(self) -> None:
        """Rollback changes to repository."""
        operator.methodcaller("rollback")(self.session)
