from django.urls import path

from f_auth import views


urlpatterns = [
    path("signup/", views.SignUp.as_view(), name="sign-up"),
    path("login/", views.Login.as_view(), name="login"),
    path("users/", views.list_users, name="users-list"),
    path("orders/", views.list_orders, name="orders-list"),
]
