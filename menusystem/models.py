import uuid

from django.contrib.auth.models import User
from django.db import models


class Menu(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    date = models.DateField(unique=True, help_text="YYYY-mm-dd format")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_dt = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"Menu for {self.date} by {self.author.username}"


class Meal(models.Model):
    name = models.CharField(max_length=100, unique=True)
    menus = models.ManyToManyField(Menu, related_name="meals")

    def __str__(self):
        return f"Meal: {self.name}"
