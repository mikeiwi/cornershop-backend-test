import pytest

from menusystem.notifiers import slack_notifier


def test_message_request(mocker):
    """When function is called, slack api post should be called"""
    slack_mock = mocker.patch("slack_sdk.WebClient.chat_postMessage")

    message = "My awesome message"
    slack_notifier(message)

    assert slack_mock.call_args.kwargs["text"] == message
