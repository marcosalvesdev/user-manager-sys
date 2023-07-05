from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from manager.models import UserProfileModel

User = get_user_model()


@receiver(post_save, sender=User, dispatch_uid="save_new_user_profile")
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfileModel.objects.create(user=instance)
