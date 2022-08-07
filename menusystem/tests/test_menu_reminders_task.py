import logging
from datetime import datetime, timedelta

import pytest
from django.conf import settings

import pytz

from menusystem.tasks import send_daily_reminder_task


@pytest.mark.django_db
def test_send_menu_reminder(menu, mocker):
    """When the task is called, a menu for the current date is sent via slack notifier."""
    office_timezone = pytz.timezone(settings.OFFICE_TIME_ZONE)
    now_date = datetime.now().astimezone(office_timezone).date()
    menu.date = now_date
    menu.save()

    mock = mocker.patch("menusystem.notifiers.slack_notifier")

    send_daily_reminder_task()

    SITE_URL = settings.SITE_URL
    menu_url = f"{SITE_URL}/menu/{menu.id}"
    mock.assert_called_once_with(f"New menu for today: {menu_url}")


@pytest.mark.django_db
def test_no_menu_for_today(menu, mocker, caplog):
    """When there's no menu for today, only a log is registered."""
    caplog.set_level(logging.WARNING)

    now_date = (datetime.now() - timedelta(days=5)).date()
    menu.date = now_date
    menu.save()

    mock = mocker.patch("menusystem.notifiers.slack_notifier")

    send_daily_reminder_task()

    assert not mock.called

    assert "No menu for today" in caplog.text
