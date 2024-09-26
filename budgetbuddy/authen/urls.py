from django.urls import path

from authen.views import LoginView, LogoutView, RegisterView, ForgotpasswordView

urlpatterns = [
    path('', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('reset-pass/', ForgotpasswordView.as_view(), name="forgot-pass"),
    path('logout/', LogoutView.as_view(), name="logout")
]