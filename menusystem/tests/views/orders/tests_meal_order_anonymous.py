import pytest
from django.urls import reverse

from model_mommy import mommy

from menusystem.models import Meal


@pytest.mark.django_db
def test_anonymous_access(client, menu):
    """Anonymous user should access the page successfully."""
    response = client.get(reverse("meal_order_create", kwargs={"pk": menu.id}))

    assert response.status_code == 200


@pytest.mark.django_db
def test_meal_options(client, menu):
    """Meal options for the menu should be displayed as options."""
    mommy.make(Meal, name="Meal not in this menu")

    response = client.get(reverse("meal_order_create", kwargs={"pk": menu.id}))

    assert b"Salad" in response.content
    assert b"Meal not in this menu" not in response.content


@pytest.mark.django_db
def test_anonymous_access_login_form(client, menu):
    """Login fields should be added to the form for unauthenticated users."""
    response = client.get(reverse("meal_order_create", kwargs={"pk": menu.id}))

    assert b"username" in response.content
    assert b"password" in response.content
