from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    host = models.CharField(max_length=60, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50, null=True)
    color = models.CharField(max_length=10, default="#989898")
    room_code = models.CharField(max_length=10, null=True)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    def __str__(self):
        return f"User-[{self.host}]-[{self.name}]"
