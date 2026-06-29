from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from user.views import CreateUserView, ManageUserView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"), # Логін (отримання токена)
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"), # Оновлення токена
    path("me/", ManageUserView.as_view(), name="manage"),
]

app_name = "user"
