# -*- coding: utf-8 -*-

# Standard Library Imports
import pathlib
import typing

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron import wrappers


@pytest.fixture
def csv_io_wrapper(
    make_csv_file: typing.Callable[[str, typing.Optional[list]], pathlib.Path],
) -> wrappers.TxtFileWrapper:
    """Fixture to make `txt` IO wrapper."""
    path = make_csv_file("test.csv", [])
    result = wrappers.CsvFileWrapper(path)
    return result


@pytest.fixture
def txt_io_wrapper(
    make_txt_file: typing.Callable[[str, typing.Optional[str]], pathlib.Path],
) -> wrappers.TxtFileWrapper:
    """Fixture to make `txt` IO wrapper."""
    path = make_txt_file("test.txt", "")
    result = wrappers.TxtFileWrapper(path)
    return result


@pytest.fixture
def xlsx_io_wrapper(
    make_xlsx_file: typing.Callable[
        [str, typing.Optional[list]], pathlib.Path
    ],
) -> wrappers.XlsxFileWrapper:
    """Fixture to make `txt` IO wrapper."""
    path = make_xlsx_file("test.xlsx", [])
    result = wrappers.XlsxFileWrapper(path)
    return result
