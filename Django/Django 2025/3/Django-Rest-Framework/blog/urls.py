from django.urls import path
from .views import PostApiView, CategoryApiView


app_name = 'blog'

urlpatterns = [
    path('post/', PostApiView.as_view()),
    path('post/update/<int:id>/', PostApiView.as_view()),
    path('category/', CategoryApiView.as_view()),
]