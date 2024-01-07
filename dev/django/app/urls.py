from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path("", include('django.contrib.auth.urls')),
    path("profile/", views.profile, name='profile')
]