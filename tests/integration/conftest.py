# -*- coding: utf-8 -*-

# Standard Library Imports
from functools import partial
import pathlib
import shutil
import tempfile
from typing import Callable
from typing import Union

# Third-Party Imports
import pytest


@pytest.fixture
def tempdir() -> str:
    """Fixture for making a temporary directory.

    Returns:
        Path of temporary directory.

    """
    tempdir = tempfile.mkdtemp()
    yield tempdir
    shutil.rmtree(tempdir)


@pytest.fixture
def make_bytes_file(tempdir: str) -> Callable[..., pathlib.Path]:
    """Fixture to make text file."""
    yield partial(make_file, pathlib.Path(tempdir), mode="wb")


@pytest.fixture
def make_text_file(tempdir: str) -> Callable[..., pathlib.Path]:
    """Fixture to make text file."""
    yield partial(make_file, pathlib.Path(tempdir), mode="w")


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

    """
    if not isinstance(__dir, pathlib.Path):
        message = f"expected type 'Path', got {type(__dir)} instead"
        raise TypeError(message)

    filepath = __dir / filename  # type: pathlib.Path
    with filepath.open(mode) as file:
        file.write(content)
        file.close()

    return filepath
