# -*- coding: utf-8 -*-

# Standard Library Imports
from datetime import datetime
from typing import Type

# Third-Party Imports
import pytest

# Local Imports
from ddd.messages import BaseMessage
from ddd.messages import BaseCommand
from ddd.messages import BaseEvent


@pytest.mark.parametrize("message_type", [BaseMessage, BaseCommand, BaseEvent])
def test_has_created_at_datetime(message_type: Type[BaseMessage]) -> None:
    result = message_type()
    assert isinstance(result.created_at, datetime)
