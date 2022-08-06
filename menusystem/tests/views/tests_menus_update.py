from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.urls import reverse

import pytz
from model_mommy import mommy

from menusystem.models import Meal, Menu


@pytest.mark.django_db
def test_no_admin_redirect(client, employee_user):
    """Employee user should be redirected."""
    menu = mommy.make(Menu)
    response = client.get(reverse("menu_update", kwargs={"pk": menu.id}))

    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_access(client, staff_user):
    """Staff user should access the page successfully with the meals."""
    menu = mommy.make(Menu)

    for i in range(4):
        meal = Meal.objects.create(name=f"Meal {i}.")
        meal.menus.add(menu)

    response = client.get(reverse("menu_update", kwargs={"pk": menu.id}))

    assert response.status_code == 200

    for i in range(4):
        assert b"Meal %a." % i in response.content


@pytest.mark.django_db
def test_basic_menu_update(client, staff_user):
    """Menu with a provided future date should be created successfully."""
    menu = Menu.objects.create(date=datetime.now().date(), author=staff_user)

    date = (datetime.now() + timedelta(days=1)).date()
    client.post(
        reverse("menu_update", kwargs={"pk": menu.id}),
        data={"date": date, "meals": "one"},
    )

    assert Menu.objects.count() == 1

    menu = Menu.objects.get()
    assert menu.date == date


@pytest.mark.django_db
def test_menu_update_after_sending_time(client, staff_user, mocker):
    """Menus reminders will be sent at a specific hour of the day. If an admin tries to
    update a menu after the sending time for the current day, the menu can not be updated."""
    SENDING_HOUR = settings.REMINDER_SENDING_HOUR
    current_hour = SENDING_HOUR + 1

    mock = mocker.patch("django.utils.timezone.now")
    mock.return_value = datetime(
        2020, 5, 3, current_hour, 0, tzinfo=pytz.timezone(settings.OFFICE_TIME_ZONE)
    )

    date = mock.return_value.date()

    menu = Menu.objects.create(date=date, author=staff_user)
    client.post(
        reverse("menu_update", kwargs={"pk": menu.id}),
        data={"date": date, "meals": "one"},
    )

    assert menu.meals.count() == 0


@pytest.mark.django_db
def test_meal_options(client, staff_user):
    """Menu meals should be stored successfully after update."""
    menu = mommy.make(Menu)

    for i in range(4):
        meal = Meal.objects.create(name=f"Meal {i}.")
        meal.menus.add(menu)

    date = (datetime.now() + timedelta(days=1)).date()

    client.post(
        reverse("menu_update", kwargs={"pk": menu.id}),
        data={
            "date": date,
            "meals": "one\r\ntwo",
        },
    )

    assert Menu.objects.count() == 1

    menu = Menu.objects.get()
    assert menu.date == date
    assert menu.meals.count() == 2

    assert Meal.objects.count() == 6
