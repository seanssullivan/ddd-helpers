# -*- coding: utf-8 -*-

# pylint: disable=arguments-renamed
# pylint: disable=missing-function-docstring

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.utils import mappers


@pytest.mark.parametrize(
    "mapper",
    [
        {"1": "one", "2": "two", "3": "three"},
        {
            "1": {"map_to": "one"},
            "2": {"map_to": "two"},
            "3": {"map_to": "three"},
        },
    ],
)
def test_applies_mapper(mapper: dict) -> None:
    data = {"1": "1", "2": "2", "3": "3"}
    result = mappers.apply_mapper(data, mapper)

    expected = {"one": "1", "two": "2", "three": "3"}
    assert result == expected


def test_applies_converters() -> None:
    data = {"1": "1", "2": "2", "3": "3"}
    mapper = {
        "1": {"map_to": "one", "converter": int},
        "2": {"map_to": "two", "converter": float},
        "3": {"map_to": "three", "converter": str},
    }
    result = mappers.apply_mapper(data, mapper)

    expected = {"one": 1, "two": 2.0, "three": "3"}
    assert result == expected


def test_does_not_include_missing_fields() -> None:
    data = {"1": "1", "2": "2", "3": "3"}
    mapper = {
        "1": {"map_to": "one"},
        "2": {"map_to": "two"},
        "3": {"map_to": "three"},
        "4": {"map_to": "four"},
    }
    result = mappers.apply_mapper(data, mapper)

    expected = {"one": "1", "two": "2", "three": "3"}
    assert result == expected


def test_includes_missing_fields_when_it_has_a_default_value() -> None:
    data = {"1": "1", "2": "2", "3": "3"}
    mapper = {
        "1": {"map_to": "one"},
        "2": {"map_to": "two"},
        "3": {"map_to": "three"},
        "4": {"map_to": "four", "default": "4"},
    }
    result = mappers.apply_mapper(data, mapper)

    expected = {"one": "1", "two": "2", "three": "3", "four": "4"}
    assert result == expected


def test_includes_missing_fields_when_required() -> None:
    data = {"1": "1", "2": "2", "3": "3"}
    mapper = {
        "1": {"map_to": "one", "required": False},
        "2": {"map_to": "two", "required": False},
        "3": {"map_to": "three", "required": False},
        "4": {"map_to": "four", "required": True},
    }
    result = mappers.apply_mapper(data, mapper)

    expected = {"one": "1", "two": "2", "three": "3", "four": None}
    assert result == expected
