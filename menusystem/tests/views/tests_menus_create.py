from datetime import datetime, timedelta

import pytest
from django.urls import reverse

from menusystem.models import Menu


@pytest.mark.django_db
def test_no_admin_redirect(client, employee_user):
    """Employee user should be redirected."""
    response = client.get(reverse("menu_create"))

    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_access(client, staff_user):
    """Staff user should access the page successfully."""
    response = client.get(reverse("menu_create"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_basic_menu_creation(client, staff_user):
    """Menu with a provided future date should be created successfully."""
    date = (datetime.now() + timedelta(days=1)).date()
    response = client.post(reverse("menu_create"), data={"date": date})

    assert Menu.objects.count() == 1

    menu = Menu.objects.get()
    assert menu.date == date
    assert menu.author == staff_user


@pytest.mark.django_db
def test_only_one_per_date(client, staff_user):
    """Only one menu should be saved per date."""
    date = (datetime.now() + timedelta(days=1)).date()
    Menu.objects.create(date=date, author=staff_user)

    response = client.post(reverse("menu_create"), data={"date": date})

    assert Menu.objects.count() == 1

    menu = Menu.objects.get()
    assert menu.date == date
    assert menu.author == staff_user
