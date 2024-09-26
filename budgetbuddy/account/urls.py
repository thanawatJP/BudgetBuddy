from django.urls import path

from account.views import *

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
]