# TODO: urls.users

from django.urls import path

from .views import UserViews

urlpatterns = [
    path('auth', UserViews.authentication, name='user-authentication'),
    path('auth-token', UserViews.refresh_auth_token, name='user-refresh-token')
]
