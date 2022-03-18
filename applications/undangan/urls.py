from django.urls import path
from .views import UndanganViews

app_name = 'api-undangan'

urlpatterns = [
    path('', UndanganViews.index),
    path('<int:id>', UndanganViews.info),
    path('<str:hashid>', UndanganViews.info),
]
