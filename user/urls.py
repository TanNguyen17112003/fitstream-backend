from django.urls import path
from .views import register_user, login_user, get_user_detail, get_users_by_role

urlpatterns = [
    path("auth/register", register_user, name="register_user"),
    path("auth/login", login_user, name="login_user"),
    path("user/<str:id>", get_user_detail, name="get_user_detail"),
    path("users/role/<str:role>", get_users_by_role, name="get_users_by_role"),
]