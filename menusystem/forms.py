from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

import pytz

from .models import Menu


class MenuForm(forms.ModelForm):
    meals = forms.CharField(
        widget=forms.Textarea(attrs={"name": "meals", "rows": 10, "cols": 80}),
        required=True,
        help_text="Split the meals in different lines.",
    )

    class Meta:
        model = Menu
        fields = ["date"]

    def clean_date(self):
        date = self.cleaned_data["date"]

        office_timezone = pytz.timezone(settings.OFFICE_TIME_ZONE)
        now = timezone.now()
        now_localized = now.astimezone(office_timezone)

        # date must be biggeer than today. If it's equal to today's date, current hour must be lower
        # than the sending hour. Otherwise the request is invalid.
        if date < now_localized.date() or (
            date == now_localized.date()
            and now_localized.hour >= settings.REMINDER_SENDING_HOUR
        ):
            raise ValidationError(
                "Sending time for this date has already passed. The manu can not be created/edited."
            )

        return date