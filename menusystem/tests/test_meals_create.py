"""Testcases for meals creation function"""
import pytest

from model_mommy import mommy
from menusystem.utils import meals_create
from menusystem.models import Meal, Menu


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
