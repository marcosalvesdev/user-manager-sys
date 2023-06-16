from django.urls import path

from manager.views import IndexView, Loginview, LogoutView, RegisterView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("index/", IndexView.as_view(), name="index"),
    path("login/", Loginview.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
]
