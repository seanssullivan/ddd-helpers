# -*- coding: utf-8 -*-

# pylint: disable=missing-function-docstring

# Third-Party Imports
import pytest

# Local Imports
from ddd.messages import BaseMessage
from ddd.queue import MessageQueue


def test_instantiates_message_queue_without_arguments() -> None:
    result = MessageQueue()
    assert isinstance(result, MessageQueue)


def test_instantiates_message_queue_with_iterable() -> None:
    result = MessageQueue([BaseMessage(), BaseMessage(), BaseMessage()])
    assert isinstance(result, MessageQueue)


def test_raises_error_when_argument_not_iterable() -> None:
    with pytest.raises(TypeError):
        MessageQueue(1)


def test_raises_error_when_argument_not_messages() -> None:
    with pytest.raises(TypeError):
        MessageQueue([1, 2, 3])


def test_sorts_messages_when_instantiated() -> None:
    message1, message2, message3 = BaseMessage(), BaseMessage(), BaseMessage()
    queue = MessageQueue([message3, message2, message1])
    assert list(queue) == [message1, message2, message3]


def test_returns_length_of_queue() -> None:
    queue = MessageQueue([BaseMessage(), BaseMessage(), BaseMessage()])
    assert len(queue) == 3


def test_returns_next_message_in_queue() -> None:
    message1, message2, message3 = BaseMessage(), BaseMessage(), BaseMessage()
    queue = MessageQueue([message1, message2, message3])
    assert next(queue) == message1


def test_raises_error_when_empty() -> None:
    queue = MessageQueue()

    with pytest.raises(StopIteration):
        next(queue)


def test_appends_to_queue() -> None:
    queue = MessageQueue([BaseMessage(), BaseMessage(), BaseMessage()])
    assert len(queue) == 3

    queue.append(BaseMessage())
    assert len(queue) == 4


def test_sorts_queue_after_appended() -> None:
    message1, message2, message3 = BaseMessage(), BaseMessage(), BaseMessage()
    queue = MessageQueue([message2, message3])
    queue.append(message1)
    assert list(queue) == [message1, message2, message3]


def test_extends_queue() -> None:
    queue = MessageQueue([BaseMessage()])
    assert len(queue) == 1

    queue.extend([BaseMessage(), BaseMessage()])
    assert len(queue) == 3


def test_sorts_queue_after_extending() -> None:
    message1, message2, message3 = BaseMessage(), BaseMessage(), BaseMessage()
    queue = MessageQueue([message3])
    queue.extend([message2, message1])
    assert list(queue) == [message1, message2, message3]


def test_returns_true_when_queue_contains_messages() -> None:
    result = MessageQueue([BaseMessage(), BaseMessage(), BaseMessage()])
    assert result


def test_returns_false_when_queue_is_empty() -> None:
    result = MessageQueue()
    assert not result


def test_loops_over_queue_until_empty() -> None:
    queue = MessageQueue([BaseMessage(), BaseMessage(), BaseMessage()])

    count = 0
    while queue:
        queue.popleft()
        count += 1

    assert not queue
    assert count == 3


def test_clears_queue() -> None:
    queue = MessageQueue([BaseMessage(), BaseMessage(), BaseMessage()])
    assert len(queue) == 3

    queue.clear()
    assert len(queue) == 0
