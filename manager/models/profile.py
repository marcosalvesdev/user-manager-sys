import os
import uuid

from django.db import models
from django.utils.translation import gettext as _


def custom_upload_to(instance, filename):
    extension = os.path.splitext(filename)[1]
    filename = f"user_{instance.user.id}_{uuid.uuid1()}_profile_picture{extension}"

    return f"profile/user_{instance.user.id}/{filename}"


class UserProfileModel(models.Model):
    OTHER = 1
    GENDER_MALE = 2
    GENDER_FEMALE = 3
    GENDER_CHOICES = [
        (OTHER, _("Other")),
        (GENDER_MALE, _("Male")),
        (GENDER_FEMALE, _("Female")),
    ]

    user = models.OneToOneField(
        "CustomUserModel", on_delete=models.CASCADE, related_name="profile"
    )
    profile_picture = models.ImageField(
        upload_to=custom_upload_to, null=True, blank=True
    )
    birthday = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(
        choices=GENDER_CHOICES, null=True, blank=True
    )
    phone = models.CharField(max_length=32, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    number = models.CharField(max_length=32, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    zip = models.CharField(max_length=30, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    def __str__(self):
        return self.user.username

    def custom_upload_to(instance, filename):
        extension = os.path.splitext(filename)[1]
        filename = f"user_{instance.user.id}_{uuid.uuid1()}_profile_picture{extension}"

        return f"profile/user_{instance.user.id}/{filename}"
