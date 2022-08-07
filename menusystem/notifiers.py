import logging
import os

from slack_sdk import WebClient

logger = logging.getLogger(__name__)


def slack_notifier(message: str):
    token = os.environ.get("SLACK_BOT_TOKEN")
    channel_id = os.environ.get("SLACK_CHANNEL_ID")

    client = WebClient(token=token)

    client.chat_postMessage(channel=channel_id, text=message)
    logger.info(f"Slack Message Sent: '{message}'")
