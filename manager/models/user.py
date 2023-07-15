from django.contrib.auth.models import AbstractUser, UserManager


class CustomUserModel(AbstractUser):
    objects = UserManager()

    class Meta(AbstractUser.Meta):
        db_table = "user"
        swappable = "AUTH_USER_MODEL"
