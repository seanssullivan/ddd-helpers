# -*- coding: utf-8 -*-

# pylint: disable=import-error
# pylint: disable=missing-function-docstring

# Standard Library Imports
import pathlib
from typing import Callable

# Third-Party
import pandas as pd
from pandas.testing import assert_frame_equal

# Local Imports
# from from dodecahedron.wrappers import DataFrameWrapper


# def test_dataframe_wrapper_can_load_from_csvfile(
#     make_csvfile: Callable,
# ) -> None:
#     rows = [["id", "value"], [1, "Test"], [2, "Test"], [3, "Test"]]
#     path = make_csvfile("test.csv", rows)  # type: pathlib.Path

#     df_wrapper = DataFrameWrapper(path.parent.resolve())
#     result = df_wrapper.load(path.name)
#     expected = pd.DataFrame(rows[1:], columns=rows[0])
#     assert_frame_equal(result, expected)


# def test_dataframe_wrapper_can_load_from_zipfile(
#     make_csvfile: Callable, make_zipfile: Callable
# ) -> None:
#     rows = [["id", "value"], [1, "Test"], [2, "Test"], [3, "Test"]]
#     path = make_zipfile(
#         "test.zip", make_csvfile("test.csv", rows)
#     )  # type: pathlib.Path

#     df_wrapper = DataFrameWrapper(path.parent.resolve())
#     result = df_wrapper.load(path.name)
#     expected = pd.DataFrame(rows[1:], columns=rows[0])
#     assert_frame_equal(result, expected)
