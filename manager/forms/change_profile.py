from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from PIL import Image

from manager.models import UserProfileModel

User = get_user_model()


def validation_profile_pic_size(image):
    img = Image.open(image)
    width, height = img.size
    if (width > 800) or (height > 800):
        raise ValidationError(
            "The profile picture has to be max 800 x 800 pixels.",
        )


class ChangeUserProfileForm(forms.ModelForm):
    profile_picture = forms.ImageField(
        validators=[validation_profile_pic_size], required=False
    )
    birthday = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
        required=False,
    )

    class Meta:
        model = UserProfileModel
        exclude = ("user",)
