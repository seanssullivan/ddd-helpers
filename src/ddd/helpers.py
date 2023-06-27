# -*- coding: utf-8 -*-

# Standard Library Imports
import functools
import inspect
from types import FunctionType
from typing import Any
from typing import Callable
from typing import Dict
from typing import List
from typing import Type
from typing import Union

# Local Imports
from .messages import AbstractMessage
from .messages import AbstractCommand
from .messages import AbstractEvent

__all__ = [
    "inject_handler_dependencies",
    "inject_dependencies",
    "raise_for_instance",
]


def inject_handler_dependencies(
    handlers: Dict[Type[AbstractMessage], Any],
    /,
    dependencies: dict,
) -> Dict[Type[AbstractMessage], Union[Callable, List[Callable[..., None]]]]:
    """Inject dependencies into handlers.

    Args:
        __handlers: Message handlers.
        dependencies: Dependencies.

    Returns:
        Handlers.

    """
    if all(isinstance(item, FunctionType) for item in handlers.values()):
        results = inject_command_handler_dependencies(handlers, dependencies)

    elif all(isinstance(item, list) for item in handlers.values()):
        results = inject_event_handler_dependencies(handlers, dependencies)

    else:
        raise NotImplementedError

    return results


def inject_command_handler_dependencies(
    handlers: Dict[Type[AbstractCommand], Callable[..., None]],
    /,
    dependencies: dict,
) -> Dict[Type[AbstractCommand], Callable[..., None]]:
    """Inject dependencies into command handlers.

    Based on 'Architecture Patterns in Python' dependency injection pattern.

    Args:
        handlers: Command handlers.
        dependencies: Dependencies.

    Returns:
        Command handlers.

    Raises:
        TypeError: when `handlers` is not type 'dict'.

    .. _Architecture Patterns in Python:
        https://github.com/cosmicpython/code

    """
    raise_for_instance(handlers, dict)
    results = {
        command_type: inject_dependencies(command_handler, dependencies)
        for command_type, command_handler in handlers.items()
    }
    return results


def inject_event_handler_dependencies(
    handlers: Dict[Type[AbstractEvent], List[Callable[..., None]]],
    /,
    dependencies: dict,
) -> Dict[Type[AbstractEvent], List[Callable[..., None]]]:
    """Inject dependencies into event handlers.

    Based on 'Architecture Patterns in Python' dependency injection pattern.

    Args:
        handlers: Event handlers.
        dependencies: Dependencies.

    Returns:
        Event handlers.

    Raises:
        TypeError: when `handlers` is not type 'dict'.

    .. _Architecture Patterns in Python:
        https://github.com/cosmicpython/code

    """
    raise_for_instance(handlers, dict)
    results = {
        event_type: [
            inject_dependencies(handler, dependencies)
            for handler in event_handlers
        ]
        for event_type, event_handlers in handlers.items()
    }
    return results


def inject_dependencies(
    handler: Callable[..., None], dependencies: dict
) -> Callable[..., None]:
    """Inject dependencies into handler function.

    Based on 'Architecture Patterns in Python' dependency injection pattern.

    Args:
        handler: Handler function.
        dependencies: Dependencies.

    .. _Architecture Patterns in Python:
        https://github.com/cosmicpython/code

    """
    params = inspect.signature(handler).parameters
    kwargs = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    result = functools.partial(handler, **kwargs)
    return result


def raise_for_instance(__obj: object, __class: type) -> None:
    """Raise error when object is not instance of provided class.

    Args:
        __obj: Object for which to check class.
        __class: Class for which to check.

    Raises:
        TypeError: when object is not an instance of class.

    """
    if not isinstance(__obj, __class):
        expected = f"expected type '{__class.__name__!s}'"
        actual = f"got {type(__obj)} instead"
        message = ", ".join([expected, actual])
        raise TypeError(message)
