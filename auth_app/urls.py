from django.urls import path
from .views import UserView, LoginUserView, UserProfileView

urlpatterns = [
    path('register/', UserView.as_view(), name="register user"),
    path('login/', LoginUserView.as_view(), name="login user"),
    path('profile/', UserProfileView.as_view(), name="user details"),
]
