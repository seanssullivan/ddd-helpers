# -*- coding: utf-8 -*-
"""File Repository."""

# Standard Library Imports
import typing

# Local Imports
from .abstract_repository import AbstractRepository

__all__ = ["AbstractFileRepository"]


class AbstractFileRepository(AbstractRepository):
    """Represents an abstract file repository.

    Args:
        __file: File.

    """

    def __init__(self, __file: typing.Any, /) -> None:
        if not isinstance(__file, typing.IO):
            message = f"expected type 'IO', got {type(__file)} instead"
            raise TypeError(message)

        self._file = __file

    def close(self) -> None:
        """Close repository."""
        self._file.close()
