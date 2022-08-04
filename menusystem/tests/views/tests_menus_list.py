"""Testcases for menus list view."""
import pytest
from django.urls import reverse

from model_mommy import mommy


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


@pytest.mark.django_db
def test_list_all_menus(client, staff_user):
    """Created menus should be listed."""
    mommy.make("Menu", author=staff_user, _quantity=3)

    response = client.get(reverse("menu"))

    assert response.status_code == 200

    context = response.context

    assert context["menu_list"].count() == 3

    assert response.content.count(b"Menu for:") == 3


@pytest.mark.django_db
def test_list_pagination(client, staff_user):
    """Menus should have a pagination strategy."""
    mommy.make("Menu", author=staff_user, _quantity=15)

    response = client.get(reverse("menu"))

    assert response.status_code == 200

    context = response.context

    assert context["menu_list"].count() == 10

    assert response.content.count(b"Menu for:") == 10

