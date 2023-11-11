# -*- coding: utf-8 -*-

# pylint: disable=missing-function-docstring

# Standard Library Imports
from typing import Any
from typing import Dict
from typing import Optional

# Third-Party Imports
# import pytest

# Local Imports
from ddd import decorators


class Child:
    def __init__(self, ref: str) -> None:
        self.ref = ref

    def __hash__(self) -> int:
        return hash(self.ref)


class Parent:
    def __init__(self, children: Optional[Dict[str, Child]] = None) -> None:
        self._objects = children or {}

    @property
    def seen(self) -> set:
        return getattr(self, "__seen__")

    @decorators.track_first_positional_argument
    def add(self, obj: object) -> None:
        if isinstance(obj, Child):
            self._objects[obj.ref] = obj

    @decorators.track_single_return_value
    def get(self, ref: str) -> Any:
        result = self._objects.get(ref)
        return result

    @decorators.track_multiple_return_values
    def list(self) -> list:
        results = list(self._objects.values())
        return results


def test_adds_argument_to_seen_objects() -> None:
    parent = Parent()
    child = Child("test")
    parent.add(child)

    assert child in parent.seen


def test_adds_returned_value_to_seen_objects() -> None:
    child1 = Child("test-1")
    child2 = Child("test-2")
    child3 = Child("test-3")
    children = [child1, child2, child3]
    parent = Parent({child.ref: child for child in children})
    parent.get("test-1")

    assert child1 in parent.seen


def test_adds_returned_values_to_seen_objects() -> None:
    child1 = Child("test-1")
    child2 = Child("test-2")
    child3 = Child("test-3")
    children = [child1, child2, child3]
    parent = Parent({child.ref: child for child in children})
    parent.list()

    assert all([child in parent.seen for child in children])
