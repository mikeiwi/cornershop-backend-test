from django.conf import settings
from menusystem.models import Menu

from typing import Callable, List


class MenuReminder:
    """Send reminders for a given menu with the provided notfiers."""
    _menu: Menu
    _notifiers: List[Callable]
    
    def __init__(self, menu: Menu, notifiers: List[Callable]):
        self._menu = menu
        self._notifiers = notifiers

    def _get_message(self):
        SITE_URL = settings.SITE_URL
        menu_url = f"{SITE_URL}/menu/{self._menu.id}"
        return f"New menu for today: {menu_url}"

    def send_reminder(self):
        for notifier in self._notifiers:
            notifier(self._get_message())
