# -*- coding: utf-8 -*-

# Standard Library Imports
import io
import pathlib
from typing import Callable

# Third-Party
import pytest


@pytest.mark.parametrize("mode", ["rb"])
def test_returns_buffered_reader_for_pdf_file(
    make_pdf_file: Callable[..., pathlib.Path], mode: str
) -> None:
    path = make_pdf_file("test.pdf", "")  # type: pathlib.Path

    file = open(path, mode=mode)
    result = isinstance(file, io.BufferedReader)
    file.close()
    assert result is True


@pytest.mark.parametrize("mode", ["wb"])
def test_returns_buffered_writer_for_pdf_file(
    make_pdf_file: Callable[..., pathlib.Path], mode: str
) -> None:
    path = make_pdf_file("test.pdf", "")  # type: pathlib.Path

    file = open(path, mode=mode)
    result = isinstance(file, io.BufferedWriter)
    file.close()
    assert result is True


@pytest.mark.parametrize("mode", ["r", "w"])
def test_returns_text_io_wrapper_for_csv_file(
    make_csv_file: Callable[..., pathlib.Path], mode: str
) -> None:
    path = make_csv_file("test.csv", [])  # type: pathlib.Path

    file = open(path, mode=mode)
    result = isinstance(file, io.TextIOWrapper)
    file.close()
    assert result is True


@pytest.mark.parametrize("mode", ["r", "w"])
def test_returns_text_io_wrapper_for_txt_file(
    make_txt_file: Callable[..., pathlib.Path], mode: str
) -> None:
    path = make_txt_file("test.txt", "")  # type: pathlib.Path

    file = open(path, mode=mode)
    result = isinstance(file, io.TextIOWrapper)
    file.close()
    assert result is True
