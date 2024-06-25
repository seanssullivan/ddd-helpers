# -*- coding: utf-8 -*-

# Standard Library Imports
import csv
import pathlib
from typing import Callable
from typing import Generator
from typing import Optional
import zipfile

# Third-Party Imports
import pytest
import xlsxwriter


@pytest.fixture
def make_csvfile(
    tempdir: str,
) -> Generator[Callable[..., pathlib.Path], None, None]:
    """Fixture to make a temporary CSV file.

    Args:
        tempdir: Temporary directory.

    """

    def _make_file(filename: str, lines: list) -> pathlib.Path:
        if not isinstance(filename, str):
            message = f"expected type 'str', got {type(filename)} instead"
            raise TypeError(message)

        path = pathlib.Path(tempdir) / filename
        with path.open("w") as file:
            writer = csv.writer(file)
            for line in lines:
                writer.writerow(line)

        return path

    yield _make_file


@pytest.fixture
def make_txtfile(
    tempdir: str,
) -> Generator[Callable[..., pathlib.Path], None, None]:
    """Fixture to make a temporary txt file.

    Args:
        tempdir: Temporary directory.

    """

    def _make_file(filename: str, content: str) -> pathlib.Path:
        if not isinstance(filename, str):
            message = f"expected type 'str', got {type(filename)} instead"
            raise TypeError(message)

        path = pathlib.Path(tempdir) / filename
        with path.open("w") as file:
            file.write(content)

        return path

    yield _make_file


@pytest.fixture
def make_xlsxfile(
    tempdir: str,
) -> Generator[Callable[..., pathlib.Path], None, None]:
    """Fixture to make a temporary xlsx file.

    Args:
        tempdir: Temporary directory.

    """

    def _make_file(
        filename: str, sheet: Optional[str] = None, *, lines: list
    ) -> pathlib.Path:
        if not isinstance(filename, str):
            message = f"expected type 'str', got {type(filename)} instead"
            raise TypeError(message)

        path = pathlib.Path(tempdir) / filename
        workbook = xlsxwriter.Workbook(path)
        worksheet = workbook.add_worksheet(sheet)

        for row, line in enumerate(lines):
            for col, item in enumerate(line):
                worksheet.write(row, col, item)

        workbook.close()
        return path

    yield _make_file


@pytest.fixture
def make_zipfile(
    tempdir: str,
) -> Generator[Callable[..., pathlib.Path], None, None]:
    """Fixture to make a temporary zip file.

    Args:
        tempdir: Temporary directory.

    """

    def _make_file(zipname: str, filepath: pathlib.Path) -> pathlib.Path:
        if not isinstance(zipname, str):
            message = f"expected type 'str', got {type(zipname)} instead"
            raise TypeError(message)

        if not isinstance(filepath, pathlib.Path):
            message = f"expected type 'Path', got {type(filepath)} instead"
            raise TypeError(message)

        zippath = pathlib.Path(tempdir) / zipname
        with zipfile.ZipFile(zippath, "w") as file:
            file.write(filepath, arcname=filepath.name)

        return zippath

    yield _make_file
