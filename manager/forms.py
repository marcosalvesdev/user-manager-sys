from django.contrib.auth.forms import BaseUserCreationForm, UsernameField
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserCreationForm(BaseUserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ("username", "email")
        field_classes = {"username": UsernameField}
