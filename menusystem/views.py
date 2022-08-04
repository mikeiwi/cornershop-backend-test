from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils.decorators import method_decorator
from django.views.generic import ListView


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class MenuListView(StaffRequiredMixin, ListView):
    """Menus List"""

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
