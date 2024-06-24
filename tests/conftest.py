# -*- coding: utf-8 -*-

# pylint: disable=missing-function-docstring

# Standard Library Imports
import shutil
import tempfile
from typing import Generator

# Third-Party Imports
import pytest


@pytest.fixture
def tempdir() -> Generator[str, None, None]:
    tempdir = tempfile.mkdtemp()
    yield tempdir
    shutil.rmtree(tempdir)
