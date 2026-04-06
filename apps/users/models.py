import uuid_utils as uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid7, editable=False)
    is_reader = models.BooleanField(default=True)
    is_writer = models.BooleanField(default=False)

    def __str__(self):
        return self.username
