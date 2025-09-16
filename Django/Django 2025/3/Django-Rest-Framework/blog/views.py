from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Post, Category
from .serializers import CategorySerializer, PostSerializer


class CategoryApiView(APIView):
    def get(self, request, *args, **kwargs):
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        context = {
            'results': {
                'message': 'Category object has been updated successfully',
                'category': serializer.data
            }
        }
        return Response(context, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        id = kwargs.get('id', None)
        if not id:
            raise Exception()
        category = get_object_or_404(Category, id=id)
        serializer = CategorySerializer(instance=category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        context = {
            'results': {
                'message': 'Post object has been updated successfully',
                'category': serializer.data
            }
        }
        return Response(context, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        id = kwargs.get('id', None)
        if not id:
            raise Exception()
        category = get_object_or_404(Category, id=id)
        serializer = CategorySerializer(instance=category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(partial=True)
        context = {
            'results': {
                'message': 'Post object has been updated successfully',
                'category': serializer.data
            }
        }
        return Response(context, status=status.HTTP_201_CREATED)

class PostApiView(APIView):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        context = {
            'results': {
                'message': 'Post object has been updated successfully',
                'post': serializer.data
            }
        }
        return Response(context, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        id = kwargs.get('id', None)
        if not id:
            raise Exception()
        post = get_object_or_404(Post, id=id)
        serializer = PostSerializer(instance=post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        context = {
            'results': {
                'message': 'Post object has been updated successfully',
                'post': serializer.data
            }
        }
        return Response(context, status=status.HTTP_201_CREATED)


    def patch(self, request, *args, **kwargs):
        id = kwargs.get('id', None)
        if not id:
            raise Exception()
        post = get_object_or_404(Post, id=id)
        serializer = PostSerializer(instance=post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(partial=True)
        context = {
            'results': {
                'message': 'Post object has been updated successfully',
                'post': serializer.data
            }
        }
        return Response(context, status=status.HTTP_201_CREATED)




