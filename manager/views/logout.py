from django.contrib.auth import views


class LogoutView(views.LogoutView):
    template_name = None
