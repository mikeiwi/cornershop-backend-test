import pytest
import pytz
from datetime import datetime
from django.conf import settings
from django.urls import reverse

from model_mommy import mommy

from menusystem.models import Meal, MealOrder


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


@pytest.mark.django_db
def test_anonymous_checkout_time_passed(client, menu, mocker):
    """An order for a given date may only be registered before chekout time (11 AM CLT).
    Request should be denied."""
    CHECKOUT_HOUR = settings.CHECKOUT_HOUR
    current_hour = CHECKOUT_HOUR + 1

    mock = mocker.patch("django.utils.timezone.now")
    mock.return_value = datetime(
        2020, 5, 3, current_hour, 0, tzinfo=pytz.timezone(settings.OFFICE_TIME_ZONE)
    )

    menu.date = mock.return_value.date()
    menu.save()
    meal = menu.meals.first()
    response = client.post(
        reverse("meal_order_create", kwargs={"pk": menu.id}), data={"meal": meal.id}
    )

    assert MealOrder.objects.count() == 0
    assert b"Checkout time has passed" in response.content
