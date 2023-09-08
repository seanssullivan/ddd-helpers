# -*- coding: utf-8 -*-

# pylint: disable=import-error
# pylint: disable=missing-function-docstring

# Standard Library Imports
import pathlib
from typing import Callable

# Third-Party Imports
# import pytest

# Local Imports
from ddd.models import File
from ddd.repositories import FileRepository


def test_saves_a_text_file(tempdir: str) -> None:
    temppath = pathlib.Path(tempdir)
    repo = FileRepository(temppath)

    file = File("test.txt", "success")
    repo.add(file)

    expected = temppath / "test.txt"
    assert expected.exists()


def test_retrieves_a_text_file(
    make_text_file: Callable[..., pathlib.Path]
) -> None:
    filepath = make_text_file("test.txt", "success")
    repo = FileRepository(filepath.parent)
    result = repo.get("test")

    expected = File("test.txt", "success")
    assert result == expected


def test_returns_none_when_file_not_found(
    make_text_file: Callable[..., pathlib.Path]
) -> None:
    filepath = make_text_file("sample.txt", "test")
    repo = FileRepository(filepath.parent)
    result = repo.get("test")
    assert not result


def test_returns_a_list_of_filenames(
    make_text_file: Callable[..., pathlib.Path]
) -> None:
    filepath1 = make_text_file("test1.txt", "one")
    filepath2 = make_text_file("test2.txt", "two")
    filepath3 = make_text_file("test3.txt", "three")
    repo = FileRepository(filepath1.parent)

    results = repo.search_filenames("*test*")

    assert sorted(results, key=lambda f: f[0]) == [
        filepath1.name,
        filepath2.name,
        filepath3.name,
    ]
