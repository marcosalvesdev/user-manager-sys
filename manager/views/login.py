from django.contrib.auth import views


class Loginview(views.LoginView):
    def get_default_redirect_url(self):
        if self.request.user.is_superuser:
            self.next_page = "/manager/"

        return super().get_default_redirect_url()
