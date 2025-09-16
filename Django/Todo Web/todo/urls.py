from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('add/', views.add_task, name='add_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('done/<int:task_id>/', views.mark_done, name='mark_done'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
]
