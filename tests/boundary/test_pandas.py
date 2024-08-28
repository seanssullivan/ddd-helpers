# -*- coding: utf-8 -*-

# pylint: disable=import-error
# pylint: disable=missing-function-docstring

# Standard Library Imports
import pathlib
from typing import Callable

# Third-Party
import pandas as pd
import pytest


def test_raises_error_when_columns_expected_but_not_found(
    make_csv_file: Callable[..., pathlib.Path]
) -> None:
    rows = [["id", "value"], ["1", "Test"], ["2", "Test"], ["3", "Test"]]
    path = make_csv_file("test.csv", rows)  # type: pathlib.Path

    with pytest.raises(ValueError, match="columns expected but not found"):
        pd.read_csv(path, usecols=["id", "value", "missing"])
