import json
from typing import Any

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth import get_user_model, mixins
from django.urls import reverse_lazy

User = get_user_model()


class MassiveUsersDeleteView(
    mixins.LoginRequiredMixin, mixins.PermissionRequiredMixin, generic.FormView
):
    template_name = "user/delete_user.html"
    success_url = reverse_lazy("manager")

    def has_permission(self) -> bool:
        user = self.request.user
        if user.is_superuser:
            return True
        return False

    def delete(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        delete_on = request.POST.get("deleteOnOff")
        users_to_delete = request.COOKIES.get("users")

        if users_to_delete and delete_on:
            users_to_delete = json.loads(users_to_delete)
            users = User.objects.filter(id__in=users_to_delete)
            users.delete()

            response = HttpResponseRedirect(self.success_url)
            response.delete_cookie("users")
            return response

        return HttpResponseRedirect(reverse_lazy("update_users"))

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return self.delete(request, *args, **kwargs)
