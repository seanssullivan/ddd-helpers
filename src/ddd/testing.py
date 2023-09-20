# -*- coding: utf-8 -*-

# Standard Library Imports
from __future__ import annotations
from typing import List
from typing import Set

# Third-Party Imports
from .models import AbstractModel
from .repositories import EventfulRepository
from .units_of_work import EventfulUnitOfWork


# Constants
COMMITTED_ATTR = "_committed"
DEFAULT_KEY = "reference"


class FakeRepository(EventfulRepository):
    def __init__(
        self,
        objects: List[AbstractModel] = None,
        key: str = DEFAULT_KEY,
    ) -> None:
        super().__init__()
        self._objects = set(objects or [])  # type: Set[AbstractModel]
        self._key = key

    def __contains__(self, obj: AbstractModel) -> bool:
        return obj in self._objects

    def add(self, obj: AbstractModel) -> None:
        """Add object."""
        self._objects.add(obj)

    def get(self, ref: str) -> AbstractModel:
        """Get object.

        Args:
            ref: Reference to object.

        """
        results = (
            obj
            for obj in self._objects
            if getattr(obj, self._key, None) == ref
        )
        return next(results, None)

    def list(self) -> List[AbstractModel]:
        """List objects."""
        return list(self._objects)

    def remove(self, obj: AbstractModel) -> None:
        """Remove object."""
        self._objects.discard(obj)

    def commit(self) -> None:
        """Commit changes."""
        pass

    def rollback(self) -> None:
        """Rollback changes."""
        pass

    def close(self) -> None:
        """Close repository."""
        pass


class FakeUnitOfWork(EventfulUnitOfWork):
    @property
    def committed(self) -> bool:
        """Whether `commit()` method was called."""
        result = getattr(self, COMMITTED_ATTR, False)
        return result

    def __enter__(self) -> FakeUnitOfWork:
        return self

    def commit(self) -> None:
        """Commit changes."""
        setattr(self, COMMITTED_ATTR, True)

    def rollback(self) -> None:
        """Rollback changes."""
