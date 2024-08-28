# -*- coding: utf-8 -*-
"""Xlsx Repository."""

# Standard Library Imports
import logging
import typing

# Local Imports
from .file_repository import AbstractFileRepository
from ..wrappers.xlsx_file_wrappers import XlsxIOWrapper

# Initiate logger.
log = logging.getLogger("dodecahedron")


class AbstractXlsxRepository(AbstractFileRepository):
    """Represents an abstract `.xlsx` file repository.

    Args:
        __file: Xlsx file.

    Attributes:
        columns: Columns names.

    """

    def __init__(self, __file: typing.IO, /) -> None:
        if not isinstance(__file, XlsxIOWrapper):
            expected = "expected type 'XlsxIOWrapper'"
            actual = f"got {type(__file)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        super().__init__(__file)

    @property
    def columns(self) -> typing.Optional[typing.Sequence]:
        """Column names."""
        results = getattr(self._file, "fieldnames", None)
        return results
