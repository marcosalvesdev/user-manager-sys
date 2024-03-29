from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

User = get_user_model()


class MassiveChangeUsersForm(forms.Form):
    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
        required=False,
    )

    is_staff = forms.BooleanField(required=False)

    is_active = forms.BooleanField(required=False)

    is_superuser = forms.BooleanField(required=False)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if not (password1 and password2):
            return None

        if password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )

        try:
            password_validation.validate_password(password2)
        except ValidationError as error:
            self.add_error("password2", error)

        return password2

    class Meta:
        fields = ("users", "password1", "password2")

    def save(self):
        user_ids = self.data.get("users_to_update", [])
        users_to_update = list()

        password = self.cleaned_data.get("password1")

        is_staff = self.cleaned_data.get("is_staff")
        remove_is_staff = self.data.get("remove_is_staff")

        is_active = self.cleaned_data.get("is_active")
        remove_is_active = self.data.get("remove_is_active")

        is_superuser = self.cleaned_data.get("is_superuser")
        remove_is_superuser = self.data.get("remove_is_superuser")

        try:
            for user_id in user_ids:
                user = User.objects.filter(id=user_id).first()
                if user:
                    if password:
                        user.set_password(password)

                    if is_staff:
                        user.is_staff = is_staff
                    elif remove_is_staff:
                        user.is_staff = False

                    if is_active:
                        user.is_active = is_active
                    elif remove_is_active:
                        user.is_active = False

                    if is_superuser:
                        user.is_superuser = is_superuser
                    elif remove_is_superuser:
                        user.is_superuser = False

                    users_to_update.append(user)

            User.objects.bulk_update(
                users_to_update, ["password", "is_staff", "is_active", "is_superuser"]
            )

        except Exception:
            raise self.add_error(
                field=None,
                error=ValidationError(
                    "Some problem occured while users updating! Please try again latter or contact our suport.",
                    code="Internal Error",
                ),
            )
