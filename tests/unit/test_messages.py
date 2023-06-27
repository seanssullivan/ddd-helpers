# -*- coding: utf-8 -*-

# pylint: disable=missing-function-docstring

# Standard Library Imports
from datetime import datetime
from typing import Type

# Third-Party Imports
import pytest

# Local Imports
from ddd.messages import BaseMessage
from ddd.messages import BaseCommand
from ddd.messages import BaseEvent


@pytest.mark.parametrize("message", [BaseMessage, BaseCommand, BaseEvent])
def test_has_created_at_datetime(message: Type[BaseMessage]) -> None:
    result = message()
    assert isinstance(result.created_at, datetime)
