# -*- coding: utf-8 -*-
"""Xlsx File Wrappers."""

# Standard Library Imports
import logging
import pathlib
from typing import Any
from typing import List
from typing import Optional
from typing import Type
from typing import TypeVar

# Third-Party Imports
from openpyxl import load_workbook
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet

# Local Imports
from .base_wrappers import BaseFileWrapper
from .base_wrappers import DEFAULT_ENCODING


# Initiate logger.
log = logging.getLogger("dodecahedron")

# Custom types
T = TypeVar("T")

# Constants
XLSX_EXTENSION = ".xlsx"


class XlsxFileWrapper(BaseFileWrapper):
    """Implements an Xlsx file wrapper.

    Args:
        filepath: Path to xlsx file.
        sheet_name (optional): Name of sheet in workbook. Default ``None``.

    Attributes:
    columns: Columns.
        filepath: Path to xlsx file.
        encoding: File encoding.

    Raises:
        ValueError: when `filepath` is not a xlsx file.

    """

    def __init__(
        self,
        filepath: pathlib.Path,
        /,
        columns: Optional[List[str]] = None,
        encoding: str = DEFAULT_ENCODING,
    ) -> None:
        if filepath.suffix.lower() != XLSX_EXTENSION:
            message = f"{filepath!s} is not a xlsx file"
            raise ValueError(message)

        super().__init__(filepath, encoding)
        self._columns = columns

    @property
    def columns(self) -> Optional[List[str]]:
        """Column names."""
        return self._columns

    def read(self, dtype: Type[T] = dict) -> List[T]:
        """Read data from xlsx file.

        Args:
            dtype (optional): Data type of returned data. Default ``dict``.

        Returns:
            Data.

        """

    def _load_worksheet(self, name: Optional[str] = None) -> Worksheet:
        """Get worksheet.

        Args:
            name (optional): Name of worksheet. Default ``None``.

        Returns:
            Worksheet.

        """
        workbook = self._load_workbook()
        result = workbook[name] if name is not None else workbook.active
        return result

    def _load_workbook(self) -> Workbook:
        """Load workbook.

        Returns:
            Workbook.

        """
        result = load_workbook(self.filepath)
        return result

    def _load(self) -> None:
        """Load objects from xlsx file."""
        for obj in self._read_contents():
            if obj.get(self._index):
                key = obj[self._index]
                self._objects[key] = obj
            else:
                log.critical("index column is empty: %s", obj)

        self._objects = self._objects.new_child()

    def _read_contents(self) -> List[dict]:
        """Read contents of an xlsx file.

        Returns:
            Contents of xlsx file.

        """
        data = load_rows(self._worksheet)
        results = make_objects(data[1:], data[0])

        if not all(self._index in row for row in results):
            log.error("index column '%s' not found", self._index)
            log.debug("available columns: %s", list(results[0].keys()))
            raise KeyError(self._index)

        return results

    def _update_worksheet(self) -> None:
        """Update worksheet."""
        recent_objects = self._objects.maps[0]
        for obj in list(recent_objects.values()):
            row = self._make_row(obj)
            self._worksheet.append(row)

        self._objects = self._objects.new_child()

    def _make_row(self, obj: object) -> List[Any]:
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

    def _save_file(self) -> None:
        """Save objects to xlsx file."""
        self._workbook.save(self.filepath)


# ----------------------------------------------------------------------------
# Helper Functions
# ----------------------------------------------------------------------------
def load_rows(__worksheet: Worksheet, /) -> List[dict]:
    """Load rows from workbook.

    Args:
        __worksheet: Workbook from which to load rows.

    Returns:
        Rows.

    """
    results = [r for r in __worksheet.iter_rows(values_only=True) if r]
    return results


def make_objects(__rows: List[list], /, columns: list) -> List[dict]:
    """Make objects.

    Args:
        __rows: Rows from which to make objects.
        columns: Column names to use as keys.

    Returns:
        Objects.

    """
    results = [make_object(row, columns) for row in __rows]
    return results


def make_object(__row: list, /, columns: list) -> dict:
    """Make object.

    Args:
        __row: Row from which to make object.
        columns: Column names to use as keys.

    Returns:
        Object.

    """
    result = {columns[idx]: value for idx, value in enumerate(__row)}
    return result
