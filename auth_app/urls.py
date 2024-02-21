from django.urls import path
from .views import UserView, LoginUserView

urlpatterns = [
    path('register/', UserView.as_view(), name="register user"),
    path('login/', LoginUserView.as_view(), name="login user")
]
