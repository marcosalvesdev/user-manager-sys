from django.contrib.auth import get_user_model, mixins
from django.views import generic

User = get_user_model()


class ListUsersView(
    mixins.LoginRequiredMixin, mixins.PermissionRequiredMixin, generic.ListView
):
    queryset = User.objects.all()
    context_object_name = "users"
