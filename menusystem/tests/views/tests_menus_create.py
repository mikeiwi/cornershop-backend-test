import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_no_admin_redirect(client, employee_user):
    """Employee user should be redirected."""
    response = client.get(reverse("menu_create"))

    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_access(client, staff_user):
    """Staff user should access the page successfully."""
    response = client.get(reverse("menu_create"))

    assert response.status_code == 200
