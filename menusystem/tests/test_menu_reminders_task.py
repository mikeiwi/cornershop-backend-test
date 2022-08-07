from datetime import datetime

import pytest
from django.conf import settings

from menusystem.tasks import send_daily_reminder_task


@pytest.mark.django_db
def test_send_menu_reminder(menu, mocker):
    """When the task is called, a menu for the current date is sent via slack notifier."""
    now_date = datetime.now().date()
    menu.date = now_date
    menu.save()

    mock = mocker.patch("menusystem.notifiers.slack_notifier")

    send_daily_reminder_task()

    SITE_URL = settings.SITE_URL
    menu_url = f"{SITE_URL}/menu/{menu.id}"
    mock.assert_called_once_with(f"New menu for today: {menu_url}")
