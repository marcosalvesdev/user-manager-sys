from typing import Any

from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth import get_user_model, mixins
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied

from manager.filters import UserFilter
from manager.forms import MassiveChangeUsersForm

User = get_user_model()


class ManagerView(
    mixins.LoginRequiredMixin, mixins.PermissionRequiredMixin, generic.ListView
):
    template_name = "manager.html"
    queryset = User.objects.all()
    model = User
    context_object_name = "users"
    paginate_by = 20
    filterset_class = UserFilter
    ordering = ("username",)
    extra_context = dict()
    change_users_form = MassiveChangeUsersForm
    object_list = None

    def get_queryset(self) -> QuerySet[Any]:
        data = self.request.GET

        self.queryset = super().get_queryset().exclude(id=self.request.user.id)

        filterset = self.filterset_class(data, queryset=self.queryset)

        self.extra_context["search_not_fount"] = False

        if filterset.qs.exists():
            self.queryset = filterset.qs
        else:
            self.extra_context["search_not_fount"] = True

        self.extra_context["filterset"] = filterset
        return self.queryset

    def has_permission(self) -> bool:
        user = self.request.user
        if user.is_superuser:
            return True
        return False

    def dispatch(self, request, *args, **kwargs):
        try:
            if not self.has_permission():
                return self.handle_no_permission()
        except PermissionDenied:
            return HttpResponseRedirect(reverse_lazy("index"))

        return super().dispatch(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        data = dict(request.POST.copy())
        data.pop("csrfmiddlewaretoken")

        user_ids = [int(user_id[0]) for user_id in data.values()]

        if not user_ids:
            return HttpResponseRedirect(reverse_lazy("manager"))

        self.template_name = "user/change_users.html"

        response = HttpResponseRedirect(reverse_lazy("update_users"))

        response.set_cookie("users", user_ids)

        return response
