import pytest
from django.contrib.auth.models import User


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
