from django.urls import path
from .views import registerUser, loginUser, logoutUser

urlpatterns = [
    path('register-user/', registerUser, name="register-user"),
    path('login-user/', loginUser, name="login-user"),
    path('logout-user/', logoutUser, name="logout-user")
]