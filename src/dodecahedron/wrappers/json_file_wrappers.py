# -*- coding: utf-8 -*-
"""JSON File Wrappers."""

# Standard Library Imports
from __future__ import annotations
import io
import json
import os
import typing

# Local Imports
from .abstract_file_wrappers import AbstractDirectoryWrapper
from .abstract_file_wrappers import AbstractFileWrapper
from .abstract_file_wrappers import AbstractTextWrapper
from ..utils import converters
from .. import settings
from .. import utils

__all__ = ["JsonDirectoryWrapper", "JsonFileWrapper"]


class AbstractJsonWrapper(AbstractTextWrapper):
    """Represents an abstract wrapper class for `.json` files."""

    def _init_json_io_wrapper(
        self,
        __buffer: memoryview,
        /,
        encoding: str = settings.DEFAULT_FILE_ENCODING,
    ) -> JsonIOWrapper:
        """Initialize I/O wrapper for `.json` file.

        Args:
            __buffer: Buffer.

        Returns:
            I/O wrapper instance.

        """
        result = JsonIOWrapper(
            __buffer,
            encoding=encoding,
        )
        setattr(result, "_context", self)
        return result


class JsonDirectoryWrapper(AbstractJsonWrapper, AbstractDirectoryWrapper):
    """Implements a wrapper for `.json` files in a directory.

    Args:
        directory: Directory from which to load `.json` file(s).
        encoding (optional): File encoding. Default `utf-8`.
        read_only (optional): Whether file is read only. Default ``False``.

    """

    def __init__(
        self,
        directory: os.PathLike,
        *,
        encoding: str = settings.DEFAULT_FILE_ENCODING,
        read_only: bool = False,
    ) -> None:
        super().__init__(
            directory,
            encoding=encoding,
            extension=settings.JSON_EXTENSION,
            read_only=read_only,
        )

    def open(self, filename: str, /, mode: str = "r") -> typing.IO:
        """Open a `.json` file and return a file object.

        Args:
            filename: Filename.
            mode (optional): Mode. Default ``r``.

        Returns:
            File object.

        Raises:
            TypeError: when `encoding` is not type ``str``.

        """

        file = super().open(filename, mode=converters.to_bytes_file_mode(mode))
        result = self._init_json_io_wrapper(file)
        return result


class JsonFileWrapper(AbstractJsonWrapper, AbstractFileWrapper):
    """Implements a wrapper for `.json` files.

    Args:
        filepath: Path to `.json` file.
        encoding (optional): File encoding. Default `utf-8`.
        read_only (optional): Whether file is read only. Default ``False``.

    Raises:
        ValueError: when `filepath` is not a `.json` file.

    """

    def __init__(
        self,
        filepath: os.PathLike,
        *,
        encoding: str = settings.DEFAULT_FILE_ENCODING,
        read_only: bool = False,
    ) -> None:
        super().__init__(
            filepath,
            encoding=encoding,
            read_only=read_only,
        )
        utils.raise_for_extension(filepath, settings.JSON_EXTENSION)

    def open(self, mode: str = "r") -> typing.IO:
        """Open the `.json` file and return a file object.

        Args:
            mode (optional): Mode. Default ``r``.

        Returns:
            File object.

        """
        file = super().open(converters.to_bytes_file_mode(mode))
        result = self._init_json_io_wrapper(file)
        return result


class JsonIOWrapper(io.TextIOWrapper):
    """Implements a I/O wrapper for `.json` files."""

    def __init__(
        self,
        buffer: memoryview,
        encoding: typing.Optional[str] = None,
        errors: typing.Optional[str] = None,
        newline: typing.Optional[str] = None,
        line_buffering: bool = False,
        write_through: bool = False,
    ) -> None:
        super().__init__(
            buffer,
            encoding=encoding,
            errors=errors,
            newline=newline,
            line_buffering=line_buffering,
            write_through=write_through,
        )
        self._context = None  # type: typing.Optional[AbstractJsonWrapper]

    def dump(self, obj: typing.Any) -> None:
        """Serialize `obj` to file."""
        json.dump(obj, self)

    def load(self) -> typing.Any:
        """Deserialize contents of file."""
        return json.load(self)
