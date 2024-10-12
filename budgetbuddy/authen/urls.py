from django.urls import path

from authen.views import LoginView, LogoutView, RegisterView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', LoginView.as_view(), name="login"),
    path('register/', RegisterView.as_view(), name="register"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="users_hub/password_reset.html"), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="users_hub/password_reset_done.html"), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users_hub/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users_hub/password_reset_complete.html'), name='password_reset_complete'),
]
