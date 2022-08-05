import pytest
from django.urls import reverse

from model_mommy import mommy

from menusystem.models import Meal, Menu


@pytest.mark.django_db
def test_no_admin_redirect(client, employee_user):
    """Employee user should be redirected."""
    menu = mommy.make(Menu)
    response = client.get(reverse("menu_update", kwargs={"pk": menu.id}))

    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_access(client, staff_user):
    """Staff user should access the page successfully with the meals."""
    menu = mommy.make(Menu)

    for i in range(4):
        meal = Meal.objects.create(name=f"Meal {i}.")
        meal.menus.add(menu)

    response = client.get(reverse("menu_update", kwargs={"pk": menu.id}))

    assert response.status_code == 200

    for i in range(4):
        assert b"Meal %a." % i in response.content
