import pytest
from django.urls import reverse

from model_mommy import mommy

from menusystem.models import Menu


@pytest.mark.django_db
def test_no_admin_redirect(client, employee_user):
    """Employee user should be redirected."""
    menu = mommy.make(Menu)
    response = client.get(reverse("menu_update", kwargs={"pk": menu.id}))

    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_access(client, staff_user):
    """Staff user should access the page successfully."""
    menu = mommy.make(Menu)
    response = client.get(reverse("menu_update", kwargs={"pk": menu.id}))

    assert response.status_code == 200
