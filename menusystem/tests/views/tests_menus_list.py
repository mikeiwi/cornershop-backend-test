"""Testcases for menus list view."""
from datetime import datetime, timedelta

import pytest
from django.urls import reverse

from model_mommy import mommy, seq


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
    date = (datetime.now() - timedelta(days=50)).date()
    mommy.make(
        "Menu", author=staff_user, _quantity=3, date=seq(date, timedelta(days=1))
    )

    response = client.get(reverse("menu"))

    assert response.status_code == 200

    context = response.context
    assert context["menu_list"].count() == 3
    assert response.content.count(b"Menu for:") == 3


@pytest.mark.django_db
def test_list_pagination(client, staff_user):
    """When there are more than 10 menus, a pagination strategy should be used."""
    date = (datetime.now() - timedelta(days=50)).date()
    mommy.make(
        "Menu", author=staff_user, _quantity=15, date=seq(date, timedelta(days=1))
    )

    response = client.get(reverse("menu"))

    assert response.status_code == 200

    context = response.context
    assert context["menu_list"].count() == 10
    assert response.content.count(b"Menu for:") == 10
