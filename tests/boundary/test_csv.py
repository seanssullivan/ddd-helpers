# -*- coding: utf-8 -*-

# Standard Library Imports
import csv
import io
import pathlib
from typing import Callable

# Third-Party
import pytest


def test_raises_unsupported_operation_error_when_reading_in_write_mode(
    make_csv_file: Callable[..., pathlib.Path]
) -> None:
    path = make_csv_file("test.csv", [])  # type: pathlib.Path

    with pytest.raises(io.UnsupportedOperation), open(path, "w") as file:
        reader = csv.reader(file)
        next(reader)


def test_raises_unsupported_operation_error_when_writing_in_read_mode(
    make_txt_file: Callable[..., pathlib.Path]
) -> None:
    path = make_txt_file("test.txt", "")  # type: pathlib.Path

    with pytest.raises(io.UnsupportedOperation), open(path, "r") as file:
        writer = csv.writer(file)
        writer.writerow(["failure"])


def test_returns_all_columns_when_no_fieldnames_provided(
    make_csv_file: Callable[..., pathlib.Path]
) -> None:
    rows = [
        ["id", "value"],
        ["1", "Test"],
        ["2", "Test"],
        ["3", "Test"],
    ]
    path = make_csv_file("test.csv", rows)  # type: pathlib.Path

    with path.open() as file:
        reader = csv.DictReader(file)
        rows = [row for row in reader]
        columns = list(rows[0].keys())

    assert columns == ["id", "value"]


def test_returns_only_requested_columns_when_fieldnames_provided(
    make_csv_file: Callable[..., pathlib.Path]
) -> None:
    rows = [
        ["id", "value", "extra"],
        ["1", "Test", ""],
        ["2", "Test", ""],
        ["3", "Test", ""],
    ]
    path = make_csv_file("test.csv", rows)  # type: pathlib.Path

    with path.open() as file:
        reader = csv.DictReader(file, ["id", "value"])
        rows = [row for row in reader]
        columns = list(rows[0].keys())

    assert columns == ["id", "value", None]


def test_returns_zero_when_no_lines_have_been_read(
    make_csv_file: Callable[..., pathlib.Path]
) -> None:
    rows = [
        ["id", "value"],
        ["1", "Test"],
        ["2", "Test"],
        ["3", "Test"],
    ]
    path = make_csv_file("test.csv", rows)  # type: pathlib.Path

    with path.open() as file:
        reader = csv.reader(file)
        result = reader.line_num

    assert result == 0
