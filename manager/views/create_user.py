from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views import generic

User = get_user_model()

from manager.forms import CustomUserCreationForm


class CreateUserView(generic.CreateView):
    template_name = "user/create_user.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("manager")
