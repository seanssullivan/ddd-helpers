# -*- coding: utf-8 -*-

# Standard Library Imports
import typing

__all__ = ["apply_mapper"]


# Constants
LOCAL = "local"
REMOTE = "remote"
TARGETS = (LOCAL, REMOTE)


def apply_mapper(
    data: dict,
    mapper: typing.Dict[str, typing.Union[dict, str]],
    target: str = REMOTE,
) -> dict:
    """Apply mapper.

    Args:
        data: Data to which to apply mapper.
        mapper: Mapper to apply to data.
        target (optional): Target. Default ``remote``.

    Returns:
        Remapped data.

    """
    if target not in TARGETS:
        raise ValueError(f"invalid target: {target}")

    std_mapper = _standardize_mapper(mapper)
    if target == LOCAL:
        return _to_local_object(data, std_mapper)

    if target == REMOTE:
        return _to_remote_object(data, std_mapper)


def _standardize_mapper(
    __mapper: typing.Dict[str, typing.Any], /
) -> typing.Dict[str, dict]:
    """Standardize mapper.

    Args:
        __mapper: Mapper to standardize.

    Returns:
        Standardized mapper.

    """
    result = {}
    for key, value in __mapper.items():
        if isinstance(value, dict):
            result[key] = value
        elif isinstance(value, str):
            result[key] = {"map_to": value}
        else:
            expected = "expected type 'dict' or 'str'"
            actual = f"got {type(value)} instead"
            message = ", ".join([expected, actual])
            raise TypeError(message)

    return result


def _to_local_object(__data: dict, /, mapper: typing.Dict[str, dict]) -> dict:
    """Remap data to local object.

    Args:
        data: Data to which to apply mapper.
        mapper: Mapper to apply to data.

    Returns:
        Local object.

    """
    result = {
        key: (
            __data[mapping["map_to"]]
            if not _is_null(__data.get(mapping["map_to"]))
            else mapping.get("default")
        )
        for key, mapping in mapper.items()
    }
    return result


def _to_remote_object(__data: dict, /, mapper: typing.Dict[str, dict]) -> dict:
    """Remap data to remote object.

    Args:
        data: Data to which to apply mapper.
        mapper: Mapper to apply to data.

    Returns:
        Remote object.

    """
    result = {
        mapping["map_to"]: (
            _apply_converter(__data[key], mapping)
            if not _is_null(__data.get(key))
            else mapping.get("default")
        )
        for key, mapping in mapper.items()
        if key in __data
        or mapping.get("default")
        or mapping.get("required", False) is True
    }
    return result


def _apply_converter(
    __value,
    /,
    mapper: typing.Dict[str, dict],
) -> typing.Any:
    """Apply converter.

    Args:
        __value: Value to convert.
        mapper: Mapper to apply to data.

    Returns:
        Converted value.

    """
    if "converter" in mapper:
        converter = mapper["converter"]  # type: typing.Callable
        result = converter(__value)
    else:
        result = __value

    return result


def _is_null(__value: typing.Any, /) -> bool:
    """Check whether value is equivalent to ``None``.

    Args:
        __value: Value to check.

    Returns:
        Whether value is equivalent to ``None``.

    """
    if __value is None:
        return True

    if isinstance(__value, str) and __value == "":
        return True

    if isinstance(__value, typing.Sequence) and not __value:
        return True

    return False
