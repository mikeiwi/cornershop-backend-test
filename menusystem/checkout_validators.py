from abc import ABC, abstractmethod
from typing import Any, Optional

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
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
    _error_handler: Handler = None
    error_message: str = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        return handler

    def set_error(self, handler: Handler) -> Handler:
        """In case you need to set the error handler (to send request to another handler instead of
        returning an error), always set the error before the next handler.

        Remember to override the handle method to make use of the error handle."""
        self._error_handler = handler
        return self

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


class IsNewOrderValidator(AbstractHandler):
    error_message = "Order for this user already exists"

    def validate(self, request: Any):
        """Validates if an order for a user does not exist."""
        return not MealOrder.objects.filter(
            menu=request["menu"], employee=request["user"]
        ).exists()


class CanAuthenticateValidator(AbstractHandler):
    def validate(self, request: Any):
        """Validates if user can be authenticated with provided credentials"""
        return authenticate(username=request["username"], password=request["password"])

    def handle(self, request: Any) -> str:
        """Let's override this method in order to set the authenticated user into the request."""
        user = self.validate(request)
        if not user:
            if self._error_handler:
                return self._error_handler.handle(request)

        elif self._next_handler:
            request["user"] = user
            return self._next_handler.handle(request)

        return None


class IsNewUserValidator(AbstractHandler):
    error_message = "User not found"

    def validate(self, request: Any):
        """Validates if a user with the username does NOT exist."""
        return not User.objects.filter(username=request["username"]).exists()
