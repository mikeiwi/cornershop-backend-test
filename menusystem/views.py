from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .forms import MenuForm
from .models import Menu
from .utils import meals_create


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class MenuListView(StaffRequiredMixin, ListView):
    """Menus List"""

    queryset = Menu.objects.order_by("-date")
    context_object_name = "menu_list"
    paginate_by = 10

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class MenuListCreateView(StaffRequiredMixin, CreateView):
    model = Menu
    form_class = MenuForm
    success_url = reverse_lazy("menu")

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        names = form.cleaned_data["meals"].split("\r\n")
        meals_create(names=names, menu=form.instance)

        return response
