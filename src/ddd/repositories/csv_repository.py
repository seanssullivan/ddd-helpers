# -*- coding: utf-8 -*-
"""CSV Repository.

Implementation based on 'Architecture Patterns in Python' repository pattern.

.. _Architecture Patterns in Python:
    https://github.com/cosmicpython/code

"""

# Standard Library Imports
import abc
import csv
import logging
import pathlib
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

# Local Imports
from .abstract_repository import AbstractRepository

__all__ = [
    "AbstractCsvRepository",
    "CsvRepository",
]


# Initiate logger.
log = logging.getLogger(__name__)


class AbstractCsvRepository(AbstractRepository):
    """Represents an abstract CSV repository."""

    @property
    @abc.abstractmethod
    def filepath(self) -> pathlib.Path:
        """Filepath."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def objects(self) -> List[object]:
        """Objects in repository."""
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def columns(self) -> List[str]:
        """Column names."""
        raise NotImplementedError


class CsvRepository(AbstractRepository):
    """Implements a CSV repository.

    This repository reads data from a CSV file.

    Args:
        __filepath: Path to CSV file.
        index: Name of column to use as index.

    Attributes:
        filepath: Path to CSV file.

    """

    def __init__(
        self, __filepath: Union[pathlib.Path, str], /, index: str = "id"
    ) -> None:
        if not isinstance(__filepath, (pathlib.Path, str)):
            expected = "expected type 'Path' or 'str'"
            actual = f"got {type(__filepath)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        if isinstance(__filepath, str):
            __filepath = pathlib.Path(__filepath)

        if not __filepath.parent.exists():
            message = f"{__filepath.parent!s} does not exist"
            raise FileNotFoundError(message)

        if __filepath.is_dir():
            message = f"{__filepath!s} is a directory"
            raise IsADirectoryError(message)

        self._filepath = __filepath
        log.debug("Set filepath as %s", self._filepath)

        self._index = index
        self._objects = {}  # type: Dict[str, dict]

        if self._filepath.exists():
            self._load()

    @property
    def filepath(self) -> pathlib.Path:
        """Filepath."""
        return self._filepath

    @property
    def objects(self) -> List[dict]:
        """Objects in repository."""
        return list(self._objects.values())

    @property
    def columns(self) -> List[str]:
        """Column names."""
        try:
            keys = next(iter(self.objects)).keys()
            results = list(keys)
        except StopIteration:
            return []
        else:
            return results

    def _load(self) -> None:
        """Load objects from CSV file."""
        for obj in self._read_contents():
            key = obj[self._index]
            self._objects[key] = obj

    def _read_contents(self) -> List[dict]:
        """Read contents of a CSV file.

        Returns:
            Contents of CSV file.

        """
        with self._filepath.open() as file:
            reader = csv.DictReader(file)
            results = [row for row in reader]

        return results

    def add(self, obj: object) -> None:
        """Add object to repository.

        Args:
            obj: Object to add to repository.

        """
        if self.can_add(obj):
            key = obj[self._index]
            self._objects[key] = obj

    def can_add(self, obj: object, /) -> bool:
        """Check whether object can be added to repository.

        Args:
            obj: Object to add to repository.

        Returns:
            Whether object can be added.

        """
        return obj[self._index] not in self._objects

    def get(self, ref: Union[int, str]) -> Optional[object]:
        """Get object from repository.

        Args:
            ref: Reference to object.

        Returns:
            Object.

        """
        result = self._objects.get(ref, None)
        return result

    def list(self) -> List[dict]:
        """List objects in repository.

        Returns:
            Objects in repository.

        """
        results = list(self._objects.values())
        return results

    def remove(self, obj: object) -> None:
        """Remove object from repository.

        Args:
            obj: Object to remove from repository.

        """
        key = obj[self._index]
        del self._objects[key]

    def commit(self) -> None:
        """Commit changes to repository."""
        self._save()

    def _save(self) -> None:
        """Save objects to CSV file."""
        with self._filepath.open("w") as file:
            writer = csv.writer(file)
            writer.writerow(self.columns)
            for obj in self.list():
                row = self._make_row(obj)
                writer.writerow(row)

    def _make_row(self, obj: object) -> list:
        """Make row.

        Args:
            obj: Object with which to make row.

        Returns:
            Row.

        """
        if not isinstance(obj, dict):
            message = f"expected type 'dict', got {type(obj)} instead"
            raise TypeError(message)

        return list(obj.values())

    def rollback(self) -> None:
        """Rollback changes to repository."""
        self._objects.clear()
        self._load()
