from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ValidationError


class CustomBaseUserManager(UserManager):
    ...


class CustomUserModel(AbstractUser):
    ...

    objects = CustomBaseUserManager

    class Meta(AbstractUser.Meta):
        db_table = "user"
        swappable = "AUTH_USER_MODEL"
