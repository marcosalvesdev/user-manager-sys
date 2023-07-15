from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)
