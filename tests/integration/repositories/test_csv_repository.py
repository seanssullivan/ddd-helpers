# -*- coding: utf-8 -*-

# pylint: disable=import-error
# pylint: disable=missing-function-docstring

# Standard Library Imports
import pathlib
from typing import Callable

# Third-Party Imports
# import pytest

# Local Imports
from dodecahedron.repositories import CsvRepository


def test_saves_a_csv_file(tempdir: str) -> None:
    temppath = pathlib.Path(tempdir)
    filepath = temppath / "test.csv"
    repo = CsvRepository(filepath)

    obj = {"id": "1", "value": "TEST"}
    repo.add(obj)
    repo.commit()

    expected = temppath / "test.csv"
    assert expected.exists()


def test_loads_a_csv_file(make_csv_file: Callable[..., pathlib.Path]) -> None:
    rows = [["id", "value"], ["1", "TEST"]]
    filepath = make_csv_file("test.csv", rows)

    repo = CsvRepository(filepath)
    result = repo.objects

    expected = [{"id": "1", "value": "TEST"}]
    assert result == expected
