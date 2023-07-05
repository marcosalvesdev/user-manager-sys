import json
from typing import Any, Dict

from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth import views, get_user_model, mixins
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied

from manager.filters import UserFilter
from manager.forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    UserChangeProfileForm,
    ChangeMultipleUsersForm,
)

from user_manager_sys.settings import ALLOWED_HOSTS

User = get_user_model()


class IndexView(generic.TemplateView):
    template_name = "index.html"


class Loginview(views.LoginView):
    def get_default_redirect_url(self):
        if self.request.user.is_superuser:
            self.next_page = "/manager/"

        return super().get_default_redirect_url()


class LogoutView(views.LogoutView):
    template_name = None


class RegisterView(generic.CreateView):
    template_name = "registration/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")


class ListUsersView(
    mixins.LoginRequiredMixin, mixins.PermissionRequiredMixin, generic.ListView
):
    queryset = User.objects.all()
    context_object_name = "users"


# TODO: IMPLEMENTAR AS VIEWS ABAIXO


class UserDetailView(mixins.LoginRequiredMixin, generic.DetailView):
    template_name = "user/user_detail.html"
    queryset = User.objects.all()
    context_object_name = "user"


class CreateUserView(generic.CreateView):
    template_name = "user/create_user.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("manager")


class UpdateUserView(
    mixins.LoginRequiredMixin, mixins.PermissionRequiredMixin, generic.UpdateView
):
    template_name = "user/update_user.html"
    queryset = User.objects.all()
    model = User
    form_class = CustomUserChangeForm
    profile_form_class = UserChangeProfileForm

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


class DeleteUserView(
    mixins.LoginRequiredMixin, mixins.PermissionRequiredMixin, generic.DeleteView
):
    template_name = "user/delete_user.html"
    queryset = User.objects.all()
    success_url = reverse_lazy("manager")

    def has_permission(self) -> bool:
        user = self.request.user
        if user.is_superuser:
            return True
        return False


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
            print(users_to_delete)
            print(type(users_to_delete))
            users = User.objects.filter(id__in=users_to_delete)
            print(users)
            users.delete()

            response = HttpResponseRedirect(self.success_url)
            response.delete_cookie("users")
            return response

        return HttpResponseRedirect(reverse_lazy("update_users"))

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return self.delete(request, *args, **kwargs)


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
    change_users_form = ChangeMultipleUsersForm
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

        print(user_ids)

        if not user_ids:
            return HttpResponseRedirect(reverse_lazy("manager"))

        self.template_name = "user/change_users.html"

        response = HttpResponseRedirect(reverse_lazy("update_users"))

        response.set_cookie("users", user_ids)

        return response


class UpdateUsersView(
    mixins.LoginRequiredMixin, mixins.PermissionRequiredMixin, generic.FormView
):
    form_class = ChangeMultipleUsersForm
    success_url = reverse_lazy("manager")
    template_name = "user/change_users.html"
    allowed_origins_requests = [
        "http://localhost:8000/manager/",
        "http://127.0.0.1:8000/manager/",
    ]

    def check_origin_request(self) -> bool:
        origin_referer = self.request.headers.get("Referer")

        if origin_referer:
            for origin in self.allowed_origins_requests:
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
