from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from .settings import STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('xol.urls')),
]