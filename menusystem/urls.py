from django.urls import path

from .views import (
    MealOrderCreateView,
    MenuCreateView,
    MenuListView,
    MenuOrderListView,
    MenuUpdateView,
)

urlpatterns = [
    path("", MenuListView.as_view(), name="menu"),
    path("/create", MenuCreateView.as_view(), name="menu_create"),
    path("/<uuid:pk>", MealOrderCreateView.as_view(), name="meal_order_create"),
    path("/<uuid:pk>/update", MenuUpdateView.as_view(), name="menu_update"),
    path("/<uuid:pk>/orders", MenuOrderListView.as_view(), name="menu_orders_list"),
]
