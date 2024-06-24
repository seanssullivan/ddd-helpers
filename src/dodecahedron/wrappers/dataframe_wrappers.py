# -*- coding: utf-8 -*-
"""DataFrame Loaders."""

# Standard Library Imports
import logging
import pathlib
import re
from typing import Callable
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

# Third-Party Imports
import pandas as pd

# Local Imports
from .base_fileloader import FileLoader
from ...domain import errors

__all__ = [
    "CsvLoader",
    "ExcelLoader",
    "remap_dataframe_columns",
]


# Initiate logger.
log = logging.getLogger(__name__)

# Constants
DEFAULT_ENCODING = "utf-8"
DEFAULT_SEPARATOR = ","


class CsvLoader(FileLoader):
    """Implements a CSV loader.

    Args:
        __dir: Path to directory.
        converters (optional): Functions for converting values.
        date_parser (optional): Function for parsing datetime columns.
        dtypes (optional): Data types into which to load data.
        encoding (optional): File encoding. Default `None`.
        na_values (optional): Additional strings to recognize as NA/NaN.
        parse_dates (optional): List of datetime columns to parse.
        usecols (optional): List of columns to use. Default `None`.

    """

    def __init__(
        self,
        __dir: pathlib.Path,
        /,
        *,
        converters: Optional[Dict[str, Callable]] = None,
        dtypes: Optional[Union[Dict[str, str], str, type]] = None,
        encoding: Optional[str] = DEFAULT_ENCODING,
        na_values: Optional[Union[Dict[str, str], List[str], str]] = None,
        parse_dates: Optional[List[str]] = None,
        usecols: Optional[List[str]] = None,
    ) -> None:
        super().__init__(__dir, encoding)
        self.converters = converters
        self.dtypes = dtypes
        self.na_values = na_values
        self.parse_dates = parse_dates
        self.usecols = usecols

    def load(
        self, __filename: str, /, sep: str = DEFAULT_SEPARATOR
    ) -> pd.DataFrame:
        """Load dataframe from file.

        Args:
            __filename: Name of file.
            sep: Separator for CSV file. Default ``,``.

        Returns:
            Pandas Dataframe.

        """
        if not isinstance(__filename, str):
            message = f"expected type `str`, got {type(__filename)!s} instead"
            raise TypeError(message)

        filepath = self._directory / __filename
        if not filepath.exists():
            filepath = self.find(__filename)

        try:
            log.debug(
                "Loading data from %(file)s...",
                {"file": filepath.name},
            )
            data = pd.read_csv(
                filepath,
                converters=self.converters,
                dtype=self.dtypes,
                encoding=self.encoding,
                index_col=False,
                na_values=self.na_values,
                parse_dates=self.parse_dates,
                sep=sep,
                usecols=self.usecols,
            )
        except ValueError as error:
            handle_value_error(error)

        return data


class ExcelLoader(FileLoader):
    """Implements an Excel loader.

    Args:
        __dir: Path to directory.
        sheet_name (optional): Name of sheet in Excel file. Default ``None``.
        converters (optional): Functions for converting values.
        date_parser (optional): Function for parsing datetime columns.
        dtypes (optional): Data types into which to load data.
        na_values (optional): Additional strings to recognize as NA/NaN.
        parse_dates (optional): List of datetime columns to parse.
        usecols (optional): List of columns to use. Default `None`.

    """

    def __init__(
        self,
        __dir: pathlib.Path,
        /,
        sheet_name: Optional[str] = None,
        *,
        converters: Optional[Dict[str, Callable]] = None,
        dtypes: Optional[Union[Dict[str, str], str, type]] = None,
        na_values: Optional[Union[Dict[str, str], List[str], str]] = None,
        parse_dates: Optional[List[str]] = None,
        usecols: Optional[List[str]] = None,
    ) -> None:
        super().__init__(__dir)
        self._sheet_name = sheet_name

        self.converters = converters
        self.dtypes = dtypes
        self.na_values = na_values
        self.parse_dates = parse_dates
        self.usecols = usecols

    def load(
        self, __filename: str, __sheet_name: Optional[str] = None, /
    ) -> pd.DataFrame:
        """Load dataframe from file.

        Args:
            __filename: Name of file.
            __sheet_name (optional): Name of sheet in Excel file. Default ``None``.

        Returns:
            Pandas Dataframe.

        """
        if not isinstance(__filename, str):
            message = f"expected type `str`, got {type(__filename)!s} instead"
            raise TypeError(message)

        filepath = self._directory / __filename
        if not filepath.exists():
            filepath = self.find(__filename)

        try:
            sheet_name = __sheet_name or self._sheet_name
            data = (
                self._load_active_sheet(filepath)
                if sheet_name is None
                else self._load_sheet_by_name(filepath, sheet_name)
            )

        except ValueError as error:
            handle_value_error(error)

        return data

    def _load_active_sheet(self, __filepath: pathlib.Path, /) -> pd.DataFrame:
        """Load data from active sheet.

        Args:
            __filepath: Path to file.

        """
        if not isinstance(__filepath, pathlib.Path):
            message = f"expected type `Path`, got {type(__filepath)!s} instead"
            raise TypeError(message)

        log.debug(
            "Loading data from %(file)s...",
            {"file": __filepath.name},
        )
        result = pd.read_excel(
            __filepath,
            converters=self.converters,
            dtype=self.dtypes,
            index_col=None,
            na_values=self.na_values,
            parse_dates=self.parse_dates,
            usecols=self.usecols,
        )
        return result

    def _load_sheet_by_name(
        self, __filepath: pathlib.Path, /, sheet_name: str
    ) -> pd.DataFrame:
        """Load data from sheet.

        Args:
            __filepath: Path to file.
            sheet_name: Name of sheet.

        """
        if not isinstance(__filepath, pathlib.Path):
            message = f"expected type `Path`, got {type(__filepath)!s} instead"
            raise TypeError(message)

        if not isinstance(sheet_name, str):
            message = f"expected type `str`, got {type(sheet_name)!s} instead"
            raise TypeError(message)

        log.debug(
            "Loading data from sheet %(sheet)s in %(file)s...",
            {"file": __filepath.name, "sheet": sheet_name},
        )
        result = pd.read_excel(
            __filepath,
            sheet_name,
            converters=self.converters,
            dtype=self.dtypes,
            index_col=None,
            na_values=self.na_values,
            parse_dates=self.parse_dates,
            usecols=self.usecols,
        )
        return result


def handle_value_error(error: Exception) -> None:
    """Handle value error.

    Args:
        error: Raised exception.

    """
    if not isinstance(error, ValueError):
        message = f"expected type 'ValueError', got {type(error)} instead"
        raise TypeError(message)

    if has_missing_columns(error):
        handle_missing_columns(error)
    else:
        raise error


def has_missing_columns(error: Exception) -> bool:
    """Check whether rrror was raised because of missing columns.

    Args:
        error: Raised exception.

    Returns:
        Whether error was raised because of missing columns.

    """
    result = re.search(r"columns (?:.*) not found", str(error))
    return bool(result)


def handle_missing_columns(error: Exception) -> None:
    """Handle missing columns.

    Args:
        error: Exception raised.

    """
    match = re.search(r"\[.*\]", str(error))
    message = (
        f"Columns not found: {match.group(0)}"
        if match
        else "columns not found"
    )
    raise errors.MissingColumns(message) from error


def remap_dataframe_columns(
    data: pd.DataFrame, mapper: Dict[str, dict]
) -> pd.DataFrame:
    """Remap column names.

    Args:
        data: Data for which to remap column names.

    Returns:
        Remapped data.

    """
    result = data.rename(
        columns={
            key: value["map_to"]
            for key, value in mapper.items()
            if value.get("map_to") is not None
        },
    )
    return result
