from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from apps.views import news, contact

from lox.settings import STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contact/', contact, name='contact'),
    path('news/', news, name='news'),
    path('', include('apps.urls'))

] + static(STATIC_URL, document_root=STATIC_ROOT) + static(MEDIA_URL, document_root=MEDIA_ROOT)
