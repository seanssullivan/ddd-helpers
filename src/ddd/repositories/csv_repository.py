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
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

# Local Imports
from .file_repository import AbstractFileRepository

__all__ = [
    "AbstractCsvRepository",
    "CsvRepository",
]


# Initiate logger.
log = logging.getLogger(__name__)


# Constants
CSV_EXTENSION = ".csv"
DEFAULT_INDEX = "id"


class AbstractCsvRepository(AbstractFileRepository):
    """Represents an abstract CSV repository."""

    @property
    @abc.abstractmethod
    def columns(self) -> List[str]:
        """Column names."""
        raise NotImplementedError


class CsvRepository(AbstractCsvRepository):
    """Implements a CSV repository.

    This repository reads data from a CSV file.

    Args:
        __filepath: Path to CSV file.
        index: Name of column to use as index.

    Attributes:
        columns: Columns names.
        filepath: Path to CSV file.
        objects: Objects in repository.

    """

    def __init__(
        self,
        __filepath: Union[pathlib.Path, str],
        /,
        index: Union[int, str] = DEFAULT_INDEX,
    ) -> None:
        if isinstance(__filepath, str):
            __filepath = pathlib.Path(__filepath)

        if __filepath.suffix.lower() != CSV_EXTENSION:
            message = f"{__filepath!s} is not a CSV file"
            raise ValueError(message)

        super().__init__(__filepath)
        self._index = index
        self._objects = {}  # type: Dict[Union[int, str], dict]

        if self._filepath.exists():
            self._load()

    @property
    def columns(self) -> List[str]:
        """Column names."""
        try:
            keys = next(iter(self.objects)).keys()
            results = list(keys)
        except StopIteration:
            return []

        return results

    @property
    def objects(self) -> List[dict]:
        """Objects in repository."""
        return list(self._objects.values())

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

    def add(self, obj: Any) -> None:
        """Add object to repository.

        Args:
            obj: Object to add to repository.

        """
        if self.can_add(obj):
            key = obj[self._index]
            self._objects[key] = obj

    def can_add(self, obj: Any, /) -> bool:
        """Check whether object can be added to repository.

        Args:
            obj: Object to add to repository.

        Returns:
            Whether object can be added.

        """
        key = obj[self._index]
        result = key not in self._objects
        return result

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

    def remove(self, obj: Any) -> None:
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
            for obj in self._objects.values():
                row = make_row(obj)
                writer.writerow(row)

    def rollback(self) -> None:
        """Rollback changes to repository."""
        self._objects.clear()
        self._load()


# ----------------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------------
def make_row(obj: object) -> List[Any]:
    """Make row.

    Args:
        obj: Object with which to make row.

    Returns:
        Row.

    """
    if not isinstance(obj, dict):
        message = f"expected type 'dict', got {type(obj)} instead"
        raise TypeError(message)

    result = list(obj.values())
    return result
