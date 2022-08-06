from datetime import datetime, timedelta

import pytest
from django.contrib.auth.models import User

from model_mommy import mommy

from menusystem.models import Meal, Menu


@pytest.fixture
def employee_user(client):
    """Use this fixture when you need all requests are performed by an employee."""
    user = User.objects.create(username="bojack")
    user.set_password("password")
    user.save()

    client.login(username="bojack", password="password")

    return user


@pytest.fixture
def staff_user(client):
    """Use this fixture when you need all requests are performed by an admin."""
    user = User.objects.create(username="mrpeanutbutter", is_staff=True)
    user.set_password("password")
    user.save()

    client.login(username="mrpeanutbutter", password="password")

    return user


@pytest.fixture
def menu():
    """Menu with meals."""
    menu = mommy.make(Menu, date=datetime.now() + timedelta(days=2))

    meal = Meal.objects.create(name="Salad")
    meal.menus.add(menu)

    meal = Meal.objects.create(name="Hamburguer")
    meal.menus.add(menu)

    return menu
