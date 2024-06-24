# -*- coding: utf-8 -*-

# Standard Library Imports
import csv
import functools
import pathlib
import shutil
import tempfile
from typing import Callable
from typing import Generator
from typing import List
from typing import Union

# Third-Party Imports
from openpyxl import Workbook
from openpyxl.worksheet.worksheet import Worksheet
import pytest


@pytest.fixture
def tempdir() -> Generator[str, None, None]:
    """Fixture for making a temporary directory.

    Returns:
        Path of temporary directory.

    """
    tempdir = tempfile.mkdtemp()
    yield tempdir
    shutil.rmtree(tempdir)


@pytest.fixture
def make_bytes_file(
    tempdir: str,
) -> Generator[Callable[..., pathlib.Path], None, None]:
    """Fixture to make text file."""
    yield functools.partial(make_file, pathlib.Path(tempdir), mode="wb")


@pytest.fixture
def make_csv_file(
    tempdir: str,
) -> Generator[Callable[..., pathlib.Path], None, None]:
    """Fixture to make CSV file."""
    yield functools.partial(make_csv, pathlib.Path(tempdir))


@pytest.fixture
def make_text_file(
    tempdir: str,
) -> Generator[Callable[..., pathlib.Path], None, None]:
    """Fixture to make text file."""
    yield functools.partial(make_file, pathlib.Path(tempdir), mode="w")


@pytest.fixture
def make_xlsx_file(
    tempdir: str,
) -> Generator[Callable[..., pathlib.Path], None, None]:
    """Fixture to make xlsx file."""
    yield functools.partial(make_xlsx, pathlib.Path(tempdir))


def make_csv(
    __dir: pathlib.Path, /, filename: str, content: List[list]
) -> pathlib.Path:
    """Make CSV.

    Args:
        __dir: Path of directory.
        filename: Name of file.
        content: Content of file.

    Returns:
        Filepath.

    """
    if not isinstance(__dir, pathlib.Path):
        message = f"expected type 'Path', got {type(__dir)} instead"
        raise TypeError(message)

    filepath = __dir / filename  # type: pathlib.Path
    with filepath.open("w") as file:
        writer = csv.writer(file)
        writer.writerow(content[0])
        for row in content[1:]:
            writer.writerow(row)

    return filepath


def make_xlsx(
    __dir: pathlib.Path, /, filename: str, content: List[list]
) -> None:
    """Make xlsx.

    Args:
        __dir: Path of directory.
        filename: Name of file.
        content: Content of file.

    Returns:
        Filepath.

    """
    if not isinstance(__dir, pathlib.Path):
        message = f"expected type 'Path', got {type(__dir)} instead"
        raise TypeError(message)

    filepath = __dir / filename  # type: pathlib.Path
    workbook = Workbook()
    worksheet = workbook.active  # type: Worksheet
    worksheet.append(content[0])
    for row in content[1:]:
        worksheet.append(row)

    workbook.save(filepath)
    return filepath


def make_file(
    __dir: pathlib.Path,
    /,
    filename: str,
    content: Union[bytes, str],
    *,
    mode: str = "w",
) -> pathlib.Path:
    """Make file.

    Args:
        __dir: Path of directory.
        filename: Name of file.
        content: Content of file.
        mode: Write mode. Default ``w``.

    Returns:
        Filepath.

    """
    if not isinstance(__dir, pathlib.Path):
        message = f"expected type 'Path', got {type(__dir)} instead"
        raise TypeError(message)

    filepath = __dir / filename  # type: pathlib.Path
    with filepath.open(mode) as file:
        file.write(content)
        file.close()

    return filepath
