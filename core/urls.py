#TODO: core.urls
from django.contrib import admin
from django.urls import include, path
from core import settings
from commands.initial_data import master

urlpatterns = []

if settings.ADMIN_ENABLED is True:
    urlpatterns += [path('admin/', admin.site.urls),]

urlpatterns += [
    path('api/init', master),
    path('api/users/', include('applications.users.urls')),
    path('api/undangan/', include('applications.undangan.urls')),
    path('api/ucapan/', include('applications.ucapan.urls')),
]
