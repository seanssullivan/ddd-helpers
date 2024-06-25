# -*- coding: utf-8 -*-

# pylint: disable=import-error
# pylint: disable=missing-function-docstring

# Standard Library Imports
import pathlib
from typing import Callable

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.wrappers import BaseFileWrapper


def test_raises_error_when_filepath_argument_is_not_path() -> None:
    with pytest.raises(TypeError, match="expected type 'Path'"):
        BaseFileWrapper("failure.txt")


def test_raises_error_when_encoding_argument_is_not_str() -> None:
    with pytest.raises(TypeError, match="expected type 'str'"):
        BaseFileWrapper(pathlib.Path("/"), 1)


def test_raises_error_when_filepath_argument_is_a_directory(
    make_txtfile: Callable[..., pathlib.Path],
) -> None:
    with pytest.raises(IsADirectoryError):
        path = make_txtfile("test.txt", "")
        BaseFileWrapper(path.parent.resolve())


def test_wrapper_can_read_from_file(
    make_txtfile: Callable[..., pathlib.Path],
) -> None:
    path = make_txtfile("test.txt", "success")

    wrapper = BaseFileWrapper(path.resolve())
    result = wrapper.read()
    assert result == "success"


def test_wrapper_can_write_to_file(
    make_txtfile: Callable[..., pathlib.Path],
) -> None:
    path = make_txtfile("test.txt", "")

    wrapper = BaseFileWrapper(path.resolve())
    wrapper.write("success")

    result = path.read_text()
    assert result == "success"
