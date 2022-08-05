from .models import Meal, Menu


def meals_create(meals: list, menu: Menu = None):
    """Bulk meals creation

    Parameters
    ----------
    meals : list
        A list of strings to create Meal objects
    menu : Menu
        If provided, all meals crated are related to the Menu
    """
    for name in meals:
        meal, _ = Meal.objects.get_or_create(name=name)

        if menu:
            meal.menus.add(menu)
