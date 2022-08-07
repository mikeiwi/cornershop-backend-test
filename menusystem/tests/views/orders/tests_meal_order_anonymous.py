from datetime import datetime

import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse

import pytz
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


@pytest.mark.django_db
def test_anonymous_existing_user_success(client, menu):
    """If provided credentials are correct, order should checkout successfully"""
    user = User.objects.create(username="princess_carolyne")
    user.set_password("meowpassword")
    user.save()

    meal = menu.meals.first()
    client.post(
        reverse("meal_order_create", kwargs={"pk": menu.id}),
        data={"meal": meal.id, "username": user.username, "password": "meowpassword"},
    )

    assert MealOrder.objects.count() == 1

    order = MealOrder.objects.get()
    assert order.menu == menu
    assert order.employee == user
    assert order.meal == meal


@pytest.mark.django_db
def test_anonymous_existing_user_existing_order(client, menu):
    """If provided credentials are correct, but order for this meal already exists, checkout should be denied."""
    user = User.objects.create(username="princess_carolyne")
    user.set_password("meowpassword")
    user.save()

    MealOrder.objects.create(employee=user, menu=menu, meal=menu.meals.last())

    meal = menu.meals.first()
    response = client.post(
        reverse("meal_order_create", kwargs={"pk": menu.id}),
        data={"meal": meal.id, "username": user.username, "password": "meowpassword"},
    )

    assert MealOrder.objects.count() == 1
    assert b"Order for this user already exists" in response.content


@pytest.mark.django_db
def test_anonymous_wrong_credentials(client, menu):
    """If provided credentials are incorrect, order should not checkout"""
    user = User.objects.create(username="princess_carolyne")
    user.set_password("meowpassword")
    user.save()

    meal = menu.meals.first()
    response = client.post(
        reverse("meal_order_create", kwargs={"pk": menu.id}),
        data={"meal": meal.id, "username": user.username, "password": "wrongpassword"},
    )

    assert MealOrder.objects.count() == 0

    assert b"User not found" in response.content


@pytest.mark.django_db
def test_signup_fow_new_user(client, menu):
    """If username is not found, a guest checkout should be performed"""
    meal = menu.meals.first()
    client.post(
        reverse("meal_order_create", kwargs={"pk": menu.id}),
        data={"meal": meal.id, "username": "new_user", "password": "password"},
    )

    assert MealOrder.objects.count() == 1

    assert User.objects.filter(username="new_user").exists()

    order = MealOrder.objects.get()
    assert order.menu == menu
    assert order.employee.username == "new_user"
    assert order.meal == meal
