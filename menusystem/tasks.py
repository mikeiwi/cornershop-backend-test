from .menu_reminder import MenuReminder
from .models import Menu


def send_daily_reminder_task():
    """Send daily menu reminder."""
    from menusystem.notifiers import slack_notifier

    menu = Menu.objects.get()

    reminder = MenuReminder(menu=menu, notifiers=[slack_notifier])
    reminder.send_reminder()
