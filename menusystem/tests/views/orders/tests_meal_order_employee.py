"""Tests cases for orders checkout by authenticated users"""
from datetime import datetime

import pytest
from django.conf import settings
from django.urls import reverse

import pytz

from menusystem.models import MealOrder


@pytest.mark.django_db
def test_employee_no_login_needed(client, menu, employee_user):
    """For an authenticated user, login fields should not be rendered."""
    response = client.get(reverse("meal_order_create", kwargs={"pk": menu.id}))

    assert b"username" not in response.content
    assert b"password" not in response.content


@pytest.mark.django_db
def test_employee_checkout_time_passed(client, menu, employee_user, mocker):
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


@pytest.mark.django_db
def test_employee_order_success(client, menu, employee_user):
    """Order should be successfully created."""
    meal = menu.meals.first()
    client.post(
        reverse("meal_order_create", kwargs={"pk": menu.id}),
        data={"meal": meal.id},
        follow=True,
    )

    assert MealOrder.objects.count() == 1

    order = MealOrder.objects.get()
    assert order.menu == menu
    assert order.employee == employee_user
    assert order.meal == meal


@pytest.mark.django_db
def test_employee_order_customization(client, menu, employee_user):
    """Optional customization shuld be stored."""
    meal = menu.meals.first()
    client.post(
        reverse("meal_order_create", kwargs={"pk": menu.id}),
        data={
            "meal": meal.id,
            "customization": "I'll pass on the posion for today, thanks.",
        },
        follow=True,
    )

    order = MealOrder.objects.get()
    assert order.customization == "I'll pass on the posion for today, thanks."


@pytest.mark.django_db
def test_employee_order_already_exists(client, menu, employee_user):
    """Employee should not be able to create more than one order for a menu."""
    MealOrder.objects.create(employee=employee_user, menu=menu, meal=menu.meals.last())

    meal = menu.meals.first()
    response = client.post(
        reverse("meal_order_create", kwargs={"pk": menu.id}),
        data={"meal": meal.id},
        follow=True,
    )

    assert MealOrder.objects.count() == 1
    assert b"Order for this user already exists" in response.content
