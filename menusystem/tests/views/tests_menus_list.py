"""Testcases for menus list view."""
import pytest
from django.urls import reverse


def test_unauthenticated_redirect(client):
    """Unauthenticated user should be redirected to login page."""
    response = client.get(reverse("menu"))

    assert response.status_code == 302


@pytest.mark.django_db
def test_no_admin_redirect(client, employee_user):
    """Employee user should be redirected."""
    response = client.get(reverse("menu"))

    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_access(client, staff_user):
    """Staff user should access the page successfully."""
    response = client.get(reverse("menu"))

    assert response.status_code == 200
