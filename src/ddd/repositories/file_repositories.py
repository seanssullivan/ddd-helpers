# -*- coding: utf-8 -*-

# Standard Library Imports
import logging
import os
import pathlib
from typing import List
from typing import Union

# Local Imports
from .abstract_repository import AbstractRepository
from ..models import File

__all__ = ["FileRepository"]


# Initiate logger.
log = logging.getLogger(__name__)


class FileRepository(AbstractRepository):
    """Implements a file repository.

    This repository reads data from files in a directory.

    Args:
        __dir: Path to directory containing files.

    """

    def __init__(self, __dir: Union[pathlib.Path, str], /) -> None:
        if not isinstance(__dir, (pathlib.Path, str)):
            expected = "expected type 'Path' or 'str'"
            actual = f"got {type(__dir)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

        if isinstance(__dir, str):
            __dir = pathlib.Path(__dir)

        if not __dir.exists() or not __dir.is_dir():
            message = f"{__dir!s} is not a valid directory"
            raise NotADirectoryError(message)

        self._directory = __dir
        log.debug("Set destination directory as %s", self._directory)

    @property
    def directory(self) -> pathlib.Path:
        """Directory of repository."""
        return self._directory

    def __contains__(self, reference: str) -> bool:
        """Check whether a file matching the reference exists in the repository.

        Args:
            reference: Substring to search for in filenames.

        Returns:
            Whether a matching file exists.

        """
        try:
            self._find_filepath(reference)
        except FileNotFoundError:
            return False
        else:
            return True

    def add(self, obj: object) -> pathlib.Path:
        """Add file to repository.

        Args:
            obj: File.

        Returns:
            Filepath.

        Raises:
            TypeError: when argument type not 'File'.

        """
        if not isinstance(obj, File):
            message = f"expected type 'File', got {type(obj)} instead"
            raise TypeError(message)

        filepath = self._make_filepath(obj.name)
        if not os.path.exists(filepath):
            with filepath.open("w") as file:
                file.write(obj.content)

        return filepath

    def get(self, ref: Union[int, str]) -> File:
        """Get file in repository.

        Args:
            ref: Reference to filename.

        Returns:
            File.

        """
        filepath = self._find_filepath(str(ref))
        content = self._read_file(filepath)
        return File(filepath.name, content)

    def _find_filepath(
        self, reference: str, extension: str = "*"
    ) -> pathlib.Path:
        """Find filepath where filename contains provided substring.

        Args:
            reference: Substring to search for in filenames.
            extension (optional): File extension with which to limit search.
                Searches all extensions when not provided.

        Returns:
            Filepath.

        Raises:
            FileNotFoundError: When no matching file found in directory.

        """
        try:
            filepath = next(
                filepath
                for filepath in self._search_filepaths(
                    reference, extension=extension
                )
            )

        except StopIteration as err:
            raise FileNotFoundError(
                f"No file matching {reference!s} found in {self.directory!s}"
            ) from err

        else:
            log.debug(
                "Found %(file)s in %(dir)s",
                {
                    "file": filepath,
                    "dir": self.directory,
                },
            )
            return filepath

    def _search_filepaths(
        self, reference: str, extension: str = "*"
    ) -> List[pathlib.Path]:
        """Search for filepaths where filenames contains provided substring.

        Args:
            reference: Substring to search for in filenames.
            extension (optional): File extension with which to limit search.
                Searches all extensions when not provided.

        Returns:
            Filepaths.

        Raises:
            FileNotFoundError: When no matching filenames found in directory.

        """

        log.debug(
            "Searching for %(ext)s files containing %(ref)s in %(dir)s",
            {
                "ref": reference,
                "ext": extension if extension != "*" else "all",
                "dir": self.directory,
            },
        )
        filename = f"{reference!s}*.{extension!s}"
        filepaths = set(self.directory.rglob(filename))

        log.debug(
            "Found %(files)s containing %(ref)s in %(dir)s",
            {
                "files": len(filepaths),
                "ref": reference,
                "dir": self.directory,
            },
        )
        result = sorted(filepaths, key=lambda p: getattr(p, "name"))
        return result

    @staticmethod
    def _read_file(filepath: pathlib.Path) -> Union[bytes, str]:
        """Read file.

        Args:
            filepath: Filepath.

        Returns:
            File content.

        """
        if filepath is None:
            raise ValueError("filepath cannot be 'None'")

        if not filepath.parent.exists():
            message = f"{filepath.parent} does not exist"
            raise FileNotFoundError(message)

        if not filepath.exists():
            message = f"{filepath.name} does not exist in {filepath.parent}"
            raise FileNotFoundError(message)

        try:
            with filepath.open("tr") as file:
                result = file.read()
        except:
            with filepath.open("rb") as file:
                result = file.read()

        return result

    def list(self, query: str, recursive=False, reverse=False) -> List[str]:
        """List files in repository.

        Args:
            query: Query to search for among filenames.
            recursive (optional): Whether to also search subdirectories.
            reverse (optional): Whether to sort results in reverse.

        Returns:
            Filenames.

        """
        filepaths = sorted(
            self.directory.glob(query)
            if not recursive
            else self.directory.rglob(query),
            reverse=reverse,
        )
        results = [path.name for path in filepaths]
        return results

    def remove(self, obj: object) -> None:
        """Remove file from repository.

        Args:
            obj: File.

        """
        if not isinstance(obj, File):
            message = f"expected type 'File', got {type(obj)} instead"
            raise TypeError(message)

        filepath = self._make_filepath(obj.name)
        if os.path.isfile(filepath):
            os.remove(filepath)

    def _make_filepath(self, filename: str) -> pathlib.Path:
        """Make filepath for filename in directory.

        Args:
            filename: Filename.

        Returns:
            Filepath.

        """
        result = self.directory / filename
        return result

    def close(self) -> None:
        """Close connection to repository."""

    def commit(self) -> None:
        """Commit changes to files in repository."""

    def rollback(self) -> None:
        """Rollback changes to files in repository"""
