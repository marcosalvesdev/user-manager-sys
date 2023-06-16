from typing import Any
from django.http import HttpRequest, HttpResponse
from django.views import generic
from django.contrib.auth import views
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from manager.forms import CustomUserCreationForm

User = get_user_model()


class IndexView(generic.TemplateView):
    template_name = "index.html"


class Loginview(views.LoginView):
    ...


class LogoutView(views.LogoutView):
    template_name = None


class RegisterView(generic.CreateView):
    template_name = "registration/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
