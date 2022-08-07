import logging

from django.conf import settings
from django.utils import timezone

import pytz

from backend_test.celery import app

from .menu_reminder import MenuReminder
from .models import Menu

logger = logging.getLogger(__name__)


@app.task
def send_daily_reminder_task():
    """Send daily menu reminder."""
    from menusystem.notifiers import slack_notifier

    office_timezone = pytz.timezone(settings.OFFICE_TIME_ZONE)
    now_date = timezone.now().astimezone(office_timezone).date()

    try:
        menu = Menu.objects.get(date=now_date)

        reminder = MenuReminder(menu=menu, notifiers=[slack_notifier])
        reminder.send_reminder()
    except Menu.DoesNotExist:
        logger.warning("No menu for today")
