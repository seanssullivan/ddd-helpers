# -*- coding: utf-8 -*-

# pylint: disable=missing-function-docstring

# Third-Party Imports
# import pytest

# Local Imports
from ddd.metaclasses import SingletonMeta


def test_subclass_is_singleton() -> None:
    class Test(metaclass=SingletonMeta):
        __singleton__ = True

        def __init__(self) -> None:
            pass

    instance1 = Test()
    instance2 = Test()
    assert instance1 is instance2


def test_clears_subclasses() -> None:
    class Test(metaclass=SingletonMeta):
        __singleton__ = True

        def __init__(self) -> None:
            pass

    instance1 = Test()
    SingletonMeta.clear()

    instance2 = Test()
    assert instance1 is not instance2


def test_discards_subclasses() -> None:
    class Test(metaclass=SingletonMeta):
        __singleton__ = True

        def __init__(self) -> None:
            pass

    instance1 = Test()
    SingletonMeta.discard(Test)

    instance2 = Test()
    assert instance1 is not instance2


def test_separate_subclasses_are_different() -> None:
    class Test1(metaclass=SingletonMeta):
        __singleton__ = True

        def __init__(self) -> None:
            pass

    class Test2(metaclass=SingletonMeta):
        __singleton__ = True

        def __init__(self) -> None:
            pass

    instance1 = Test1()
    instance2 = Test2()
    assert instance1 is not instance2
