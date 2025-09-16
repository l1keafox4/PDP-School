from django.urls import path
from .views import UserList, UsersDelete

urlpatterns = [
    path('', UserList.as_view(), name="home"),
    path('<int:pk>/', UsersDelete.as_view(), name='delete'),
]

