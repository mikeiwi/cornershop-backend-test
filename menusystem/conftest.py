import pytest
from django.contrib.auth.models import User


@pytest.fixture
def employee_user(client):
    """Use this fixture when you need all requests are performed by an employee."""
    user = User.objects.create(username="bojack")
    user.set_password("password")
    user.save()

    client.login(username='bojack', password='password')

    return user
