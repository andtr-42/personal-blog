from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied
from django.db import transaction

from .models import CustomUser


def user_create(
    *, username: str, email: str, password: str, is_reader: bool, is_writer: bool
) -> CustomUser:
    hashed_password = make_password(password)

    with transaction.atomic():
        if CustomUser.objects.filter(username=username).exists():
            raise PermissionDenied(
                f"A user with the username '{username}' already exists."
            )

        user = CustomUser.objects.create(
            username=username,
            email=email,
            password=hashed_password,
            is_reader=is_reader,
            is_writer=is_writer,
        )

        return user
