# -*- coding: utf-8 -*-

# pylint: disable=import-error
# pylint: disable=missing-function-docstring

# Standard Library Imports
import pathlib
from typing import Callable

# Local Imports
from dodecahedron.wrappers import CsvFileWrapper


def test_wrapper_can_read_from_csvfile(
    make_csvfile: Callable[..., pathlib.Path],
) -> None:
    rows = [
        ["id", "value"],
        ["1", "One"],
        ["2", "Two"],
        ["3", "Three"],
    ]
    path = make_csvfile("test.csv", rows)

    wrapper = CsvFileWrapper(path.resolve())
    result = wrapper.read()
    expected = [
        {"id": "1", "value": "One"},
        {"id": "2", "value": "Two"},
        {"id": "3", "value": "Three"},
    ]
    assert result == expected
