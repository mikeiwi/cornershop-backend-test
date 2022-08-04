import uuid

from django.contrib.auth.models import User
from django.db import models


class Menu(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    date = models.DateField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_dt = models.DateTimeField(auto_now_add=True, null=True)
