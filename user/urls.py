from django.urls import path

from user import views

app_name = "user"

urlpatterns = [
    path("users/create/", views.CreateUserView.as_view(), name="create-user"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("token/", views.get_access_token, name="token"),
    path("users/list/", views.UserList.as_view(), name="user-list"),
]
