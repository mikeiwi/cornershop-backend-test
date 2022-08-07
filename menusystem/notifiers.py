import logging
import os

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)


def slack_notifier(message: str):
    token = os.environ.get("SLACK_BOT_TOKEN")
    channel_id = os.environ.get("SLACK_CHANNEL_ID")

    client = WebClient(token=token)

    try:
        client.chat_postMessage(channel=channel_id, text=message)
        logger.info(f"Slack Message Sent: '{message}'")
    except SlackApiError as e:
        logger.error(f"Error sending message: {e}")
