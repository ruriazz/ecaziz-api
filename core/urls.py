from django.contrib import admin
from django.urls import include, path
from core import settings

urlpatterns = []

if settings.ADMIN_ENABLED is True:
    urlpatterns += [path('admin/', admin.site.urls),]

urlpatterns += [
    path('api/undangan/', include('undangan.urls'), name='api-undangan'),
    path('api/ucapan/', include('ucapan.urls'), name='api-ucapan'),
]
