# -*- coding: utf-8 -*-

# pylint: disable=missing-function-docstring

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
def make_csvfile(tempdir: str) -> Generator[Callable, None, None]:
    def _make_csv(filename: str, lines) -> pathlib.Path:
        path = pathlib.Path(tempdir) / filename
        with path.open("w") as file:
            writer = csv.writer(file)
            for line in lines:
                writer.writerow(line)
        return path

    yield _make_csv


@pytest.fixture
def make_xlsxfile(tempdir: str) -> Generator[Callable, None, None]:
    def _make_xlsx(
        filename: str, sheet: Optional[str] = None, *, lines: list
    ) -> pathlib.Path:
        path = pathlib.Path(tempdir) / filename
        workbook = xlsxwriter.Workbook(path)
        worksheet = workbook.add_worksheet(sheet)

        for row, line in enumerate(lines):
            for col, item in enumerate(line):
                worksheet.write(row, col, item)

        workbook.close()
        return path

    yield _make_xlsx


@pytest.fixture
def make_zipfile(tempdir: str) -> Generator[Callable, None, None]:
    def _make_zip(zipname: str, filepath) -> pathlib.Path:
        zippath = pathlib.Path(tempdir) / zipname
        content = pathlib.Path(filepath)
        with zipfile.ZipFile(zippath, "w") as file:
            file.write(content, arcname=content.name)
        return zippath

    yield _make_zip
