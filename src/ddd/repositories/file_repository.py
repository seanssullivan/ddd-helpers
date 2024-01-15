# -*- coding: utf-8 -*-
"""File Repository."""

# Standard Library Imports
import abc
import logging
import pathlib
from typing import Union

# Local Imports
from .abstract_repository import AbstractRepository

__all__ = ["AbstractFileRepository"]


# Initiate logger.
log = logging.getLogger(__name__)


class AbstractFileRepository(AbstractRepository):
    """Represents an abstract file repository.

    Args:
        __filepath: Path to file.
        index: Name of column to use as index.

    Attributes:
        filepath: Path to file.
        objects: Objects in repository.

    """

    def __init__(self, __filepath: Union[pathlib.Path, str], /) -> None:
        if not isinstance(__filepath, (pathlib.Path, str)):
            expected = "expected type 'Path' or 'str'"
            actual = f"got {type(__filepath)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        if isinstance(__filepath, str):
            __filepath = pathlib.Path(__filepath)

        if not __filepath.parent.exists():
            message = f"{__filepath.parent!s} does not exist"
            raise FileNotFoundError(message)

        if __filepath.is_dir():
            message = f"{__filepath!s} is a directory"
            raise IsADirectoryError(message)

        self._filepath = __filepath
        log.debug("Set filepath as %s", self._filepath)

    @property
    def filepath(self) -> pathlib.Path:
        """Filepath."""
        return self._filepath

    @property
    @abc.abstractmethod
    def objects(self) -> list:
        """Objects in repository."""
        raise NotImplementedError
