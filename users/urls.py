# TODO: urls.users

from django.urls import path

from .views import UserViews

urlpatterns = [
    path('auth/', UserViews.authentication, name='user-authentication')
]
