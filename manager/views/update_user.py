from typing import Any, Dict

from django.http import HttpRequest, HttpResponse
from django.views import generic
from django.contrib.auth import get_user_model, mixins
from django.urls import reverse_lazy

from manager.forms import ChangeUserProfileForm, CustomChangeUserForm

User = get_user_model()


class UpdateUserView(
    mixins.LoginRequiredMixin, mixins.PermissionRequiredMixin, generic.UpdateView
):
    template_name = "user/update_user.html"
    queryset = User.objects.all()
    model = User
    form_class = CustomChangeUserForm
    profile_form_class = ChangeUserProfileForm

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        user = self.get_object()
        profile_form = self.profile_form_class(instance=user.profile)

        kwargs.update({"profile_form": profile_form})

        return super().get_context_data(**kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        user = self.get_object()

        data = self.request.POST
        files = self.request.FILES

        user_form = self.form_class(data=data, instance=user)
        profile_form = self.profile_form_class(
            data=data, files=files, instance=user.profile
        )

        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()

            profile_form = self.profile_form_class(
                data=profile_form.cleaned_data, instance=user.profile
            )
        else:
            profile_form.data = profile_form.cleaned_data

        return self.render_to_response(
            context={
                "form": user_form,
                "profile_form": profile_form,
            }
        )

    def get_success_url(self) -> str:
        user = self.get_object()
        self.success_url = reverse_lazy("update_user", kwargs={"pk": user.id})
        return super().get_success_url()

    def has_permission(self) -> bool:
        user_to_update = self.get_object()
        session_user = self.request.user

        if session_user.is_superuser or (session_user.id == user_to_update.id):
            return True

        return False
