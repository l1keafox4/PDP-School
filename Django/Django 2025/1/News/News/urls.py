"""
URL configuration for News project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from post.views import *
from main.views import *
from account.views import *
from News.settings import STATIC_URL, STATIC_ROOT, MEDIA_URL, MEDIA_ROOT


urlpatterns = [
    path('admin/', admin.site.urls),
    path('contact/', contact, name='contact'),
    path('', home, name='home'),
    path('news/', news_view, name='home'),

]+ static(STATIC_URL, document_root=STATIC_ROOT) + static(MEDIA_URL, document_root=MEDIA_ROOT)

