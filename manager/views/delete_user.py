from django.contrib.auth import get_user_model, mixins
from django.urls import reverse_lazy
from django.views import generic

User = get_user_model()


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
