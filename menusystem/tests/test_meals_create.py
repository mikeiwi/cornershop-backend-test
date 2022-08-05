"""Testcases for meals creation function"""
import pytest

from model_mommy import mommy

from menusystem.models import Meal, Menu
from menusystem.utils import meals_create


@pytest.mark.django_db
def test_meal_creation():
    """Meals should be saved successfully."""
    meals = ["Chicken with Rice.", "Radioactive Hamburgers."]

    meals_create(meals=meals)

    assert Meal.objects.count() == 2


@pytest.mark.django_db
def test_menu_relation():
    """When a Menu is provided, the meals get related to this menu."""
    meals = ["Radioactive Hamburgers."]

    menu = mommy.make(Menu)
    meals_create(meals=meals, menu=menu)

    assert Meal.objects.get().menus.filter(id=menu.id).exists()


@pytest.mark.django_db
def test_existing_meal():
    """If a meal exists,the existing meal is related to the menu."""
    meals = ["Radioactive Hamburgers."]
    Meal.objects.create(name=meals[0])

    menu = mommy.make(Menu)
    meals_create(meals=meals, menu=menu)

    assert Meal.objects.get().menus.filter(id=menu.id).exists()
