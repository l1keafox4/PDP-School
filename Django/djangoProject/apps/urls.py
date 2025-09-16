from django.urls import path
from apps.views import home, news
from django.conf.urls.static import static





urlpatterns = [
    path('', home, name='home'),


]
