from django.urls import path

from manager.views import (
    IndexView,
    Loginview,
    LogoutView,
    RegisterView,
    ListUsersView,
    UserDetailView,
    CreateUserView,
    UpdateUserView,
    DeleteUserView,
    ManagerView,
    MassiveUsersUpdateView,
    MassiveUsersDeleteView,
)


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("index/", IndexView.as_view(), name="index"),
    path("login/", Loginview.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("list_users/", ListUsersView.as_view(), name="list-users"),
    path("user_detail/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("create_user/", CreateUserView.as_view(), name="create_user"),
    path("update_user/<int:pk>/", UpdateUserView.as_view(), name="update_user"),
    path("delete_user/<int:pk>/", DeleteUserView.as_view(), name="delete_user"),
    path("manager/", ManagerView.as_view(), name="manager"),
    path("update_users/", MassiveUsersUpdateView.as_view(), name="update_users"),
    path(
        "delete_user/massive/",
        MassiveUsersDeleteView.as_view(),
        name="massive_users_delete",
    ),
]
