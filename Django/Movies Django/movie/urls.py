from django.contrib import admin
from django.urls import path
from films import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('add/', views.add_movie, name='add_movie'),
    path('remove/<int:movie_id>/', views.remove_movie, name='remove_movie'),
]
