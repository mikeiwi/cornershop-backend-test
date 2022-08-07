import pytest
from django.urls import reverse

from model_mommy import mommy


@pytest.mark.django_db
def test_employee_cant_access(client, employee_user, menu):
    """Employee should not be able to see orders."""
    response = client.get(reverse("menu_orders_list", kwargs={"pk": menu.id}))

    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_access(client, staff_user, menu):
    """Admin should be abled to access orders page."""
    response = client.get(reverse("menu_orders_list", kwargs={"pk": menu.id}))

    assert response.status_code == 200


@pytest.mark.django_db
def test_menu_orders(client, staff_user, menu):
    """Only orders for the menu should be listed."""
    mommy.make("menusystem.MealOrder", menu=menu)
    mommy.make("menusystem.MealOrder")

    response = client.get(reverse("menu_orders_list", kwargs={"pk": menu.id}))

    context = response.context
    assert context["mealorder_list"].count() == 1
    assert response.content.count(b"Order for:") == 1
