from django.urls import path

from .views import *

app_name = 'post'

urlpatterns = [
    path('index/', index, name='index'),
    path('<int:id>/', post_detail, name='detail'),
    path('category/<int:id>/', category_detail, name='category_detail')
]
