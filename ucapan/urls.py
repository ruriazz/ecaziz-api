from django.urls import path
from .views import test

app_name = 'api-ucapan'

urlpatterns = [
    path('', test)
]