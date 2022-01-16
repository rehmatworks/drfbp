from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    RegisterView, UserView, PasswordResetView, PasswordUpdateView)
from django.urls import path

app_name='accounts'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='user_register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('identity/', UserView.as_view(), name='user_view'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset_view'),
    path('password-update/', PasswordUpdateView.as_view(), name='update_password_view'),
]