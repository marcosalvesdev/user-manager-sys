from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomChangeUserForm(forms.ModelForm):
    id = forms.CharField(
        required=False, disabled=True, widget=forms.TextInput(attrs={"type": "hidden"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user_form_checkbox_fields = {
            "is_active": self.instance.is_active,
            "is_staff": self.instance.is_staff,
            "is_superuser": self.instance.is_superuser,
        }

        for field_name, field_value in user_form_checkbox_fields.items():
            if field_value is True:
                self.fields[field_name].widget.attrs["checked"] = "checked"
            else:
                self.fields[field_name].widget.attrs.pop("checked", None)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "is_superuser",
        )

        help_texts = {"email": "We'll never share your email with anyone else."}

        labels = {
            "is_active": "Active User",
            "is_staff": "Is Staff",
            "is_superuser": "Is Superuser",
        }
