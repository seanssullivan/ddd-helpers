# -*- coding: utf-8 -*-

# pylint: disable=import-error
# pylint: disable=missing-function-docstring

# Standard Library Imports
import pathlib
from typing import Callable
from typing import Optional

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.wrappers.json_file_wrappers import JsonFileWrapper
from dodecahedron.wrappers.json_file_wrappers import JsonIOWrapper


def test_opening_file_returns_json_io_wrapper(
    make_json_file: Callable[[str, Optional[dict]], pathlib.Path],
) -> None:
    path = make_json_file("test.json", {})
    wrapper = JsonFileWrapper(path.resolve())
    result = wrapper.open()
    assert isinstance(result, JsonIOWrapper)


def test_returned_io_wrapper_is_not_closed(
    make_json_file: Callable[[str, Optional[dict]], pathlib.Path],
) -> None:
    path = make_json_file("test.json", "")
    wrapper = JsonFileWrapper(path.resolve())
    result = wrapper.open()
    assert not result.closed


def test_can_be_passed_to_builtin_open_function(
    make_json_file: Callable[[str, Optional[dict]], pathlib.Path],
) -> None:
    path = make_json_file("test.json", "")
    wrapper = JsonFileWrapper(path.resolve())
    open(wrapper).close()


def test_raises_error_when_filepath_argument_is_not_path() -> None:
    with pytest.raises(TypeError, match="expected type 'PathLike'"):
        JsonFileWrapper("failure.json")


def test_raises_error_when_encoding_argument_is_not_str(
    make_json_file: Callable[[str, Optional[dict]], pathlib.Path],
) -> None:
    with pytest.raises(TypeError, match="expected type 'str'"):
        path = make_json_file("test.json", "")
        JsonFileWrapper(path, encoding=1)


def test_raises_error_when_filepath_argument_is_a_directory(
    make_json_file: Callable[[str, Optional[dict]], pathlib.Path],
) -> None:
    with pytest.raises(IsADirectoryError):
        path = make_json_file("test.json", "")
        JsonFileWrapper(path.parent.resolve())


def test_raises_error_when_file_does_not_have_json_extension(
    tempdir: str,
) -> None:
    path = pathlib.Path(tempdir) / "text.csv"
    with pytest.raises(ValueError, match="not a '.json' file"):
        JsonFileWrapper(path.resolve())
