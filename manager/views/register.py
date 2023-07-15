from django.urls import reverse_lazy
from django.views import generic

from manager.forms import CustomUserCreationForm


class RegisterView(generic.CreateView):
    template_name = "registration/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
