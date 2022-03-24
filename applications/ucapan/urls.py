from django.urls import path

from applications.ucapan.views import UcapanViews

app_name = 'api-ucapan'

urlpatterns = [
    path('', UcapanViews.index),
    path('status/<int:id>', UcapanViews.status_change),
    path('<int:id>', UcapanViews.posts),
]