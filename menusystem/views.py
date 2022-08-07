from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView

from .forms import MealOrderForm, MealOrderFormUnauthenticated, MenuForm
from .models import MealOrder, Menu
from .utils import meals_create


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class MenuListView(StaffRequiredMixin, ListView):
    """Menus List"""

    queryset = Menu.objects.order_by("-date")
    context_object_name = "menu_list"
    paginate_by = 10


class MenuCreateView(StaffRequiredMixin, CreateView):
    model = Menu
    form_class = MenuForm
    success_url = reverse_lazy("menu")

    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)

        meals = form.cleaned_data["meals"].split("\r\n")
        meals_create(meals=meals, menu=form.instance)

        return response


class MenuUpdateView(StaffRequiredMixin, UpdateView):
    model = Menu
    form_class = MenuForm
    success_url = reverse_lazy("menu")

    def form_valid(self, form):
        response = super().form_valid(form)

        form.instance.meals.clear()
        meals = form.cleaned_data["meals"].split("\r\n")
        meals_create(meals=meals, menu=form.instance)

        return response


class MealOrderCreateView(CreateView):
    """Order checkout view"""

    model = MealOrder

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        menu = Menu.objects.get(id=self.kwargs["pk"])
        context["form"].fields["meal"].queryset = menu.meals.all()
        return context

    def get_form_class(self):
        if self.request.user.is_authenticated:
            return MealOrderForm

        return MealOrderFormUnauthenticated

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs["menu"] = Menu.objects.get(id=self.kwargs["pk"])
        return kwargs

    def get_success_url(self):
        return reverse_lazy("")

    def form_valid(self, form):
        form.instance.employee = form.cleaned_data["employee"]
        form.instance.menu = form.menu
        form.instance.save()

        messages.success(
            self.request, f"Your meal: <b>{form.instance.meal.name}</b> was registered!"
        )
        return HttpResponseRedirect(self.request.path_info)


class MenuOrderListView(StaffRequiredMixin, ListView):
    """Employee orders by menu"""

    paginate_by = 10

    def get_queryset(self):
        return MealOrder.objects.filter(menu=self.kwargs["pk"])
