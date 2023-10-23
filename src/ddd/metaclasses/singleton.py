# -*- coding: utf-8 -*-

# Standard Library Imports
from __future__ import annotations
import abc
from typing import Dict

__all__ = ["SingletonMeta"]


class SingletonMeta(abc.ABCMeta):
    """Implements a singleton metaclass.

    The singleton metaclass allows subclasses to act as singletons.

    By implementing the singleton pattern using a metaclass, instead of within
    the `__new__` method, we avoid calling `__init__` each time a subclass is
    instantiated.

    Notes:
        * Subclasses will only behave as singletons when they contain a
        `__singleton__` attribute which is set to ``True``.

    """

    _instances: Dict[str, object] = {}

    def __call__(cls, *args, **kwargs) -> object:
        key = get_hashkey(cls)

        if key not in cls._instances:
            instance = super().__call__(*args, **kwargs)

            if cls.is_singleton(instance):
                cls._instances[key] = instance

        result = cls._instances[key]
        return result

    @classmethod
    def clear(cls) -> None:
        """Clear all instances of subclasses."""
        cls._instances.clear()

    @classmethod
    def discard(cls, subclass: type) -> None:
        """Discard an instance of a subclass.

        Args:
            subclass: Subclass to discard.

        """
        key = get_hashkey(subclass)
        if cls._instances.get(key):
            del cls._instances[key]

    @staticmethod
    def is_singleton(__obj: object, /) -> bool:
        """Checks whether an object is a singleton.

        Args:
            __obj: Object.

        Returns:
            Whether object is a singleton.

        """
        result = getattr(__obj, "__singleton__", False)  # type: bool
        return result


def get_hashkey(__cls: type, /) -> str:
    """Get hash key for class.

    Args:
        __cls: Class for which to get hash key.

    Returns:
        Hash key.

    """
    result = make_hashkey(__cls.__module__, __cls.__name__)
    return result


def make_hashkey(*args) -> str:
    """Generate a hash key.

    Args:
        *args: Positional arguments.

    Returns:
        Hash key.

    """
    result = str(hash(args))
    return result
