# -*- coding: utf-8 -*-
"""CSV File Wrappers."""

# Standard Library Imports
import csv
import logging
import pathlib
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar

# Local Imports
from .base_wrappers import BaseFileWrapper
from .base_wrappers import DEFAULT_ENCODING

__all__ = ["CsvFileWrapper"]


# Initiate logger.
log = logging.getLogger("dodecahedron")

# Custom types
T = TypeVar("T")

# Constants
CSV_EXTENSION = ".csv"


class CsvFileWrapper(BaseFileWrapper):
    """Implements a CSV file wrapper.

    Args:
        filepath: Path to CSV file.
        encoding (optional): File encoding. Default `utf-8`.
        index: Name of column to use as index.

    Attributes:
        columns: Columns.
        filepath: Path to CSV file.
        encoding: File encoding.

    Raises:
        ValueError: when `filepath` is not a CSV file.

    """

    def __init__(
        self,
        filepath: pathlib.Path,
        /,
        columns: Optional[List[str]] = None,
        encoding: str = DEFAULT_ENCODING,
    ) -> None:
        if filepath.suffix.lower() != CSV_EXTENSION:
            message = f"{filepath!s} is not a CSV file"
            raise ValueError(message)

        super().__init__(filepath, encoding)
        self._columns = columns

    @property
    def columns(self) -> Optional[List[str]]:
        """Column names."""
        return self._columns

    def read(self, dtype: Type[T] = dict) -> List[T]:
        """Read data from CSV file.

        Args:
            dtype (optional): Data type of returned data. Default ``dict``.

        Returns:
            Data.

        """
        if dtype is dict:
            return self._read_each_row_as_dict()

        if dtype is list:
            return self._read_each_row_as_list()

        raise NotImplementedError

    def _read_each_row_as_dict(self) -> List[Dict[str, Any]]:
        """Read data from CSV file as list of dictionaries.

        Returns:
            Data.

        """
        with self._filepath.open(encoding=self._encoding) as file:
            reader = csv.DictReader(file)
            results = [row for row in reader]

        if not self._columns:
            self._columns = get_columns(results)

        return results

    def _read_each_row_as_list(self) -> List[list]:
        """Read data from CSV file as list of lists.

        Returns:
            Data.

        """
        with self._filepath.open(encoding=self._encoding) as file:
            reader = csv.reader(file)
            rows = [row for row in reader]
            columns, results = rows[0], rows[1:]

        if not self._columns:
            self._columns = columns

        return results

    def write(self, data: list) -> None:
        """Write data to CSV file.

        Args:
            data: Data to write to file.

        """
        if not isinstance(data, list):
            message = f"expected type 'list', got {type(data)} instead"
            raise TypeError(message)

        if all(isinstance(_, dict) for _ in data):
            self._write_each_row_from_dict(data)

        if all(isinstance(_, list) for _ in data):
            self._write_each_row_from_list(data)

        raise NotImplementedError

    def _write_each_row_from_dict(self, data: List[dict]) -> None:
        """Write data to CSV file from list of dictionaries.

        Args:
            data: Data to write to CSV file.

        """
        if not isinstance(data, list):
            message = f"expected type 'list', got {type(data)} instead"
            raise TypeError(message)

        if not all(isinstance(_, dict) for _ in data):
            message = "all items in list must be type 'dict'"
            raise TypeError(message)

        with self._filepath.open(
            "w", encoding=self._encoding, newline=""
        ) as file:
            writer = csv.DictWriter(file, fieldnames=self.columns)

            writer.writeheader()
            for item in data:
                writer.writerow(item)

    def _write_each_row_from_list(self, data: List[list]) -> None:
        """Write data to CSV file from list of lists.

        Args:
            data: Data to write to CSV file.

        """
        with self._filepath.open(
            "w", encoding=self._encoding, newline=""
        ) as file:
            writer = csv.writer(file)
            writer.writerow(self.columns)
            for row in data:
                writer.writerow(row)


# ----------------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------------
def get_columns(data: List[dict]) -> List[str]:
    """Get columns from data.

    Args:
        data: Data for which to get columns.

    Returns:
        Columns.

    """
    results = [key for key in data[0].keys()]
    return results
