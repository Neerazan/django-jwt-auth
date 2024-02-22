from django.urls import path
from .views import UserView, LoginUserView, UserProfileView, UserChangePasswordView, SendPasswordResetEmailView, UserPasswordRestView

urlpatterns = [
    path('register/', UserView.as_view(), name="register-user"),
    path('login/', LoginUserView.as_view(), name="login-user"),
    path('profile/', UserProfileView.as_view(), name="user-details"),
    path('change_password/', UserChangePasswordView.as_view(), name="change-password"),
    path('reset_password/', SendPasswordResetEmailView.as_view(), name="reset_password"),
    path('reset/<uid>/<token>/', UserPasswordRestView.as_view(), name='password-rest-view')
]
