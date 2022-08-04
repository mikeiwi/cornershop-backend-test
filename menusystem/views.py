from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import ListView

from .models import Menu


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class MenuListView(StaffRequiredMixin, ListView):
    """Menus List"""

    queryset = Menu.objects.all()
    context_object_name = "menu_list"

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
