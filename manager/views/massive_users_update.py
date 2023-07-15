import json
from typing import Any

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth import get_user_model, mixins
from django.urls import reverse_lazy
from manager.forms import MassiveChangeUsersForm

from user_manager_sys.settings import ALLOWED_HOSTS, DEBUG, IS_PRODUCTION

User = get_user_model()


class MassiveUsersUpdateView(
    mixins.LoginRequiredMixin, mixins.PermissionRequiredMixin, generic.FormView
):
    form_class = MassiveChangeUsersForm
    success_url = reverse_lazy("manager")
    template_name = "user/change_users.html"

    def allowed_origins_requests(self):
        return [f"https://{host}/manager/" for host in ALLOWED_HOSTS]

    def check_origin_request(self) -> bool:
        if DEBUG and not IS_PRODUCTION:
            return True

        origin_referer = self.request.headers.get("Referer")
        print(origin_referer)

        if origin_referer:
            for origin in self.allowed_origins_requests():
                if origin in origin_referer:
                    return True

        return False

    def has_permission(self) -> bool:
        user = self.request.user

        if user.is_authenticated and user.is_active and user.is_superuser:
            return True
        return False

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if not self.check_origin_request():
            return HttpResponseRedirect(self.success_url)

        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        users_to_update = request.COOKIES.get("users")

        data = request.POST.copy()

        if not users_to_update:
            return HttpResponseRedirect(self.success_url)

        data["users_to_update"] = json.loads(users_to_update)

        form = self.form_class(data)

        if form.is_valid():
            try:
                form.save()
            except Exception:
                return self.form_invalid(form)

            response = HttpResponseRedirect(self.success_url)
            response.delete_cookie("users")
            return response

        return self.form_invalid(form)
