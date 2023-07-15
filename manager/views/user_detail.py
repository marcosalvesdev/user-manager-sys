from django.contrib.auth import get_user_model, mixins
from django.views import generic

User = get_user_model()


class UserDetailView(mixins.LoginRequiredMixin, generic.DetailView):
    template_name = "user/user_detail.html"
    queryset = User.objects.all()
    context_object_name = "user"
