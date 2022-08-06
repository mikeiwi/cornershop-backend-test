from abc import ABC, abstractmethod
from typing import Any, Optional

from django.conf import settings
from django.utils import timezone

import pytz

from menusystem.models import MealOrder


class Handler(ABC):
    @abstractmethod
    def set_next(self, handler):
        pass

    @abstractmethod
    def handle(self, request) -> Optional[str]:
        pass

    @abstractmethod
    def validate(self, request) -> Optional[str]:
        pass


class AbstractHandler(Handler):
    """
    Base Validator Handler.
    """

    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return handler

    def handle(self, request: Any) -> str:
        if not self.validate(request):
            return self.error_message
        elif self._next_handler:
            return self._next_handler.handle(request)

        return None


class CheckoutTimeValidator(AbstractHandler):
    error_message = "Checkout time has passed"

    def validate(self, request: Any):
        """Validates if the checkout hour has already passed for the menu."""
        CHECKOUT_HOUR = settings.CHECKOUT_HOUR
        menu = request["menu"]

        office_timezone = pytz.timezone(settings.OFFICE_TIME_ZONE)
        now = timezone.now()
        now_localized = now.astimezone(office_timezone)

        menu_checkout_datetime = timezone.datetime(
            menu.date.year,
            menu.date.month,
            menu.date.day,
            CHECKOUT_HOUR,
            0,
            tzinfo=office_timezone,
        )

        return now_localized < menu_checkout_datetime


class ExistingOrderValidator(AbstractHandler):
    error_message = "Order for this user already exists"

    def validate(self, request: Any):
        """Validates if an order for a user does not exist."""
        return not MealOrder.objects.filter(
            menu=request["menu"], employee=request["user"]
        ).exists()
