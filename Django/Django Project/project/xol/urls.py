from django.urls import path
from xol.views import Home
from django.conf.urls.static import static



urlpatterns = [
    path('', Home, name="home"),
]

