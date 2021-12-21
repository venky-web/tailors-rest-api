from django.urls import path

from user import views

app_name = "user"

urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create-user"),
    path("token/", views.LoginView.as_view(), name="token"),
    path("users/", views.UserList.as_view(), name="user-list"),
]
