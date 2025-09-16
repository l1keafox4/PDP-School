from django.urls import path
from django.contrib import admin
from . import views
urlpatterns = [
    path('create/', views.ContactCreateView.as_view(), name='contact_create'),
    path('update/<int:pk>/', views.ContactUpdateView.as_view(), name='contact_update'),
    path('delete/<int:pk>/', views.ContactDeleteView.as_view(), name='contact_delete'),
    path('admin/', admin.site.urls),
    path('', views.Contact.as_view(), name='contact'),
]