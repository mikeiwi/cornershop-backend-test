from django.urls import path

from .views import MenuCreateView, MenuListView, MenuUpdateView

urlpatterns = [
    path("", MenuListView.as_view(), name="menu"),
    path("/create", MenuCreateView.as_view(), name="menu_create"),
    path("/<uuid:pk>/update", MenuUpdateView.as_view(), name="menu_update"),
]
