from django.urls import path

from .views import DashboardView

app_name = 'api-dashboard'

urlpatterns = [
    path('', DashboardView.index)
]