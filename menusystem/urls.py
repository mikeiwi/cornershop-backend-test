from django.urls import path

from .views import MenuListCreateView, MenuListView

urlpatterns = [
    path("", MenuListView.as_view(), name="menu"),
    path("/create", MenuListCreateView.as_view(), name="menu_create"),
]
