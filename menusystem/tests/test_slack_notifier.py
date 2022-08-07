import logging

from slack_sdk.errors import SlackApiError

from menusystem.notifiers import slack_notifier


def test_message_request(mocker):
    """When function is called, slack api post should be called"""
    slack_mock = mocker.patch("slack_sdk.WebClient.chat_postMessage")

    message = "My awesome message"
    slack_notifier(message)

    assert slack_mock.call_args.kwargs["text"] == message


def test_logging_success(mocker, caplog):
    """On slack post success, an info message should be logged"""
    caplog.set_level(logging.INFO)
    mocker.patch("slack_sdk.WebClient.chat_postMessage")

    message = "My awesome message"
    slack_notifier(message)

    assert f"Slack Message Sent: '{message}'" in caplog.text


def test_logging_error(mocker, caplog):
    """On slack post error, an error message should be logged"""
    caplog.set_level(logging.ERROR)
    slack_mock = mocker.patch("slack_sdk.WebClient.chat_postMessage")
    slack_mock.side_effect = SlackApiError("error message", {})

    message = "My awesome message"
    slack_notifier(message)

    assert "error message" in caplog.text
