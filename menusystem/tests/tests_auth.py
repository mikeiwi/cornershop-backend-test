import pytest
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
def test_login_render(client):
    """A login page is rendered"""
    response = client.get(reverse("login"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_login_successful(client):
    """A user should be able to log in."""
    user = User.objects.create(is_staff=True, username="mrpeanutbutter")
    user.set_password("password")
    user.save()

    response = client.post(
        reverse("login"), {"username": "mrpeanutbutter", "password": "password"}
    )

    assert response.status_code == 302


@pytest.mark.django_db
def test_logout(client):
    """A logout page should be accessible."""
    response = client.get(reverse("logout"))

    assert response.status_code == 302
