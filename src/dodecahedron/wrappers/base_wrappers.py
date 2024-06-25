# -*- coding: utf-8 -*-
"""Base Wrappers."""

# Standard Library Imports
from __future__ import annotations
import logging
import pathlib
from typing import Literal
from typing import Type
from typing import TypeVar
from typing import Union

# Local Imports
from .abstract_wrapper import AbstractWrapper

__all__ = ["BaseDirectoryWrapper", "BaseFileWrapper"]


# Initiate logger.
log = logging.getLogger("dodecahedron")

# Custom types
T = TypeVar("T")

# Constants
DEFAULT_ENCODING = "utf-8"


class BaseDirectoryWrapper(AbstractWrapper):
    """Implements a directory wrapper.

    Args:
        __dir: Directory from which to load file(s).
        encoding (optional): File encoding. Default `utf-8`.

    Raises:
        TypeError: when `directory` is not type ``Path``.
        TypeError: when `encoding` is not type ``str``.
        NotADirectoryError: when `directory` is not a valid directory.

    """

    def __new__(
        cls: Type[T],
        directory: pathlib.Path,
        /,
        encoding: str = DEFAULT_ENCODING,
    ) -> T:
        if not isinstance(directory, pathlib.Path):
            message = f"expected type 'Path', got {type(directory)} instead"
            raise TypeError(message)

        if not isinstance(encoding, str):
            message = f"expected type 'str', got {type(encoding)} instead"
            raise TypeError(message)

        if directory and (not directory.exists() or not directory.is_dir()):
            message = f"{directory!s} is not a valid directory"
            raise NotADirectoryError(message)

        return super().__new__(cls)

    def __init__(
        self,
        directory: pathlib.Path,
        /,
        encoding: str = DEFAULT_ENCODING,
    ) -> None:
        self._directory = directory
        log.debug("Set directory as %s", self._directory)

        self._encoding = encoding
        log.debug("Set expected file encoding to %s", self._encoding)

    @property
    def directory(self) -> pathlib.Path:
        """Path to directory."""
        return self._directory

    @property
    def encoding(self) -> str:
        """Expected file encoding."""
        return self._encoding

    def read(
        self, filename: str, /, *, mode: Literal["r", "rb"] = "r"
    ) -> Union[bytes, str]:
        """Read data from file.

        Args:
            filename: Name of file.
            mode (optional): Mode in which to open file. Default ``r``.

        Returns:
            File content.

        Raises:
            TypeError: when `filename` is not type ``str``.

        """
        if not isinstance(filename, str):
            message = f"expected type 'str', got {filename} instead"
            raise TypeError(message)

        if mode not in ("r", "rb"):
            message = f"mode must be either 'r' or 'rb', not {mode}"
            raise ValueError(message)

        filepath = self._directory / filename
        if not filepath.exists():
            filepath = self.find(filename)

        with filepath.open(mode, encoding=self.encoding) as file:
            return file.read()

    def find(self, ref: str) -> pathlib.Path:
        """Find path for file in directory.

        Finds the filepath for a file in the source directory where the
        filename contains the provided substring.

        Args:
            ref: Substring for which to search.

        Returns:
            Path for file.

        Raises:
            FileNotFoundError: When no filenames match provided substring.

        """
        log.debug(
            "Searching for %(ref)s in %(dir)s",
            {"ref": ref, "dir": self._directory},
        )

        try:
            filename = f"*{ref!s}*.*" if "." not in ref else ref
            filepath = next(path for path in self._directory.rglob(filename))

        except StopIteration as err:
            message = f"{self._directory / filename} not found"
            raise FileNotFoundError(message) from err

        else:
            log.debug("Found %s", filepath)
            return filepath

    def write(
        self,
        filename: str,
        /,
        data: Union[bytes, str],
        *,
        mode: Literal["w", "wb"] = "w",
    ) -> None:
        """Write data to file in directory.

        Args:
            filename: Name of file.
            data: Data to write to file.
            mode (optional): Mode in which to open file. Default ``w``.

        Raises:
            TypeError: when `filename` is not type ``str``.

        """
        if not isinstance(filename, str):
            message = f"expected type 'str', got {filename} instead"
            raise TypeError(message)

        if mode not in ("w", "wb"):
            message = f"mode must be either 'w' or 'wb', not {mode}"
            raise ValueError(message)

        filepath = self._directory / filename
        with filepath.open(mode, encoding=self.encoding) as file:
            file.write(data)


class BaseFileWrapper(AbstractWrapper):
    """Implements a file wrapper.

    Args:
        filepath: Path to file.
        encoding (optional): File encoding. Default `utf-8`.

    Raises:
        TypeError: when `filepath` is not type ``Path``.
        TypeError: when `encoding` is not type ``str``.
        FileNotFoundError: when file does not exist.
        IsADirectoryError: when `filepath` points to a directory.

    """

    def __new__(
        cls: Type[T],
        filepath: pathlib.Path,
        /,
        encoding: str = DEFAULT_ENCODING,
    ) -> T:
        if not isinstance(filepath, pathlib.Path):
            message = f"expected type 'Path', got {type(filepath)} instead"
            raise TypeError(message)

        if not isinstance(encoding, str):
            message = f"expected type 'str', got {type(encoding)} instead"
            raise TypeError(message)

        if filepath.is_dir():
            message = f"{filepath!s} is a directory"
            raise IsADirectoryError(message)

        return super().__new__(cls)

    def __init__(
        self,
        filepath: pathlib.Path,
        /,
        encoding: str = DEFAULT_ENCODING,
    ) -> None:
        self._filepath = filepath
        log.debug("Set filepath as %s", self._filepath)

        self._encoding = encoding
        log.debug("Set expected file encoding to %s", self._encoding)

    @property
    def filepath(self) -> pathlib.Path:
        """Path to file."""
        return self._filepath

    @property
    def encoding(self) -> str:
        """Expected file encoding."""
        return self._encoding

    def read(self, *, mode: Literal["r", "rb"] = "r") -> Union[bytes, str]:
        """Read data from file.

        Args:
            mode (optional): Mode in which to open file. Default ``r``.

        Returns:
            File content.

        Raises:
            ValueError: when `mode` is not ``r`` or ``rb``.
            FileNotFoundError: when file does not exist.

        """
        if mode not in ("r", "rb"):
            message = f"mode must be either 'r' or 'rb', not {mode}"
            raise ValueError(message)

        if not self.filepath.exists():
            message = f"{self.filepath!s} does not exist"
            raise FileNotFoundError(message)

        with self.filepath.open(mode, encoding=self.encoding) as file:
            return file.read()

    def write(
        self, data: Union[bytes, str], *, mode: Literal["w", "wb"] = "w"
    ) -> None:
        """Write data to file.

        Args:
            data: Data to write to file.
            mode (optional): Mode in which to open file. Default ``w``.

        """
        if mode not in ("w", "wb"):
            message = f"mode must be either 'w' or 'wb', not {mode}"
            raise ValueError(message)

        with self.filepath.open(mode, encoding=self.encoding) as file:
            file.write(data)
