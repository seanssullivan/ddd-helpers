# -*- coding: utf-8 -*-

# pylint: disable=import-error
# pylint: disable=missing-function-docstring

# Standard Library Imports
import typing

# Third-Party Imports
import pytest

# Local Imports
from dodecahedron.repositories import AbstractCsvRepository
from dodecahedron.wrappers import AbstractFileWrapper


class ExampleRepository(AbstractCsvRepository):

    def __init__(
        self, __file: typing.IO, objects: typing.Optional[list] = None
    ) -> None:
        super().__init__(__file)
        self._objects = set(objects or [])

    def __contains__(self, obj: object) -> bool:
        return obj in self._objects

    def add(self, obj: object) -> None:
        """Add object."""
        self._objects.add(obj)

    def get(self, _: str) -> object:
        """Get object."""
        raise NotImplementedError

    def list(self) -> list:
        """List objects."""
        raise NotImplementedError

    def remove(self, _: object) -> None:
        """Remove object."""
        raise NotImplementedError

    def commit(self) -> None:
        """Commit changes."""

    def rollback(self) -> None:
        """Rollback changes."""


@pytest.mark.parametrize("name", ["txt_io_wrapper", "xlsx_io_wrapper"])
def test_raises_error_when_not_a_csv_file(
    name: str, request: pytest.FixtureRequest
) -> None:
    with pytest.raises(TypeError, match="expected type 'CsvIOWrapper'"):
        wrapper = request.getfixturevalue(name)  # type: AbstractFileWrapper
        with wrapper.open() as file:
            ExampleRepository(file)


# def test_saves_a_csv_file(tempdir: str) -> None:
#     temppath = pathlib.Path(tempdir)
#     filepath = temppath / "test.csv"
#     repo = CsvBasedRepository(filepath)

#     obj = {"id": "1", "value": "TEST"}
#     repo.add(obj)
#     repo.commit()

#     expected = temppath / "test.csv"
#     assert expected.exists()


# def test_loads_a_csv_file(make_csv_file: Callable[..., pathlib.Path]) -> None:
#     rows = [["id", "value"], ["1", "TEST"]]
#     filepath = make_csv_file("test.csv", rows)

#     repo = CsvBasedRepository(filepath)
#     result = repo.objects

#     expected = [{"id": "1", "value": "TEST"}]
#     assert result == expected
