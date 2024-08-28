# -*- coding: utf-8 -*-

# Standard Library Imports
import io
import pathlib
from typing import Callable

# Third-Party
import pytest


def test_raises_unsupported_operation_error_when_reading_in_write_mode(
    make_txt_file: Callable[..., pathlib.Path]
) -> None:
    path = make_txt_file("test.txt", "")  # type: pathlib.Path

    with pytest.raises(io.UnsupportedOperation), open(path, "w") as file:
        file.read()


def test_raises_unsupported_operation_error_when_writing_in_read_mode(
    make_txt_file: Callable[..., pathlib.Path]
) -> None:
    path = make_txt_file("test.txt", "")  # type: pathlib.Path

    with pytest.raises(io.UnsupportedOperation), open(path, "r") as file:
        file.write("")


def test_reads_remaining_lines(
    make_txt_file: Callable[..., pathlib.Path]
) -> None:
    path = make_txt_file("test.txt", "one\ntwo\nthree\n")  # type: pathlib.Path

    with open(path, "r") as file:
        file.readline()
        result = file.readlines()

    expected = ["two\n", "three\n"]
    assert result == expected
