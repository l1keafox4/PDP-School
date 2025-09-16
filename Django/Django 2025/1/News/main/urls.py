from django.urls import path
from main.views import *
from django.conf.urls.static import static





urlpatterns = [
    path('', home, name='home'),

]
