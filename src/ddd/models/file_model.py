# -*- coding: utf-8 -*-
"""File model."""

# pylint: disable=too-few-public-methods

# Standard Library Imports
from typing import Union

# Local Imports
from .abstract_models import AbstractModel

__all__ = ["File"]


class File(AbstractModel):
    """Implements a file model."""

    def __init__(self, name: str, content: Union[bytes, str]) -> None:
        self.name = name
        self.content = content

    @property
    def name(self) -> str:
        """Name of file."""
        return self._filename

    @name.setter
    def name(self, value: str) -> None:
        if not isinstance(value, str):
            message = f"expected type 'str', got {type(value)} instead"
            raise TypeError(message)

        self._filename = value

    @property
    def content(self) -> Union[bytes, str]:
        """Content of file."""
        return self._content

    @content.setter
    def content(self, value: str) -> None:
        if not isinstance(value, (bytes, str)):
            expected = "expected type 'bytes' or 'str'"
            actual = f"got {type(value)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        self._content = value

    def __eq__(self, other: object) -> bool:
        result = (
            (other.name, other.content) == (self.name, self.content)
            if isinstance(other, File)
            else False
        )
        return result

    def __hash__(self) -> int:
        return hash(self.name)
