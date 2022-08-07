import pytest
from django.urls import reverse


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
