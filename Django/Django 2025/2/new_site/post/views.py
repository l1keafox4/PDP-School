from django.shortcuts import *

from .models import Category, Post

from django.http import Http404
from django.utils import timezone
from django.contrib.auth import get_user_model
from random import choice, randint
import random


from .models import Post
User = get_user_model()
    


def index(request):
    posts = Post.objects.filter(status=Post.Status.PUBLISHED)[:5]
    index_cats = Category.objects.filter(is_active=True, is_index=True)[:3]
    first_cat_posts = Post.objects.filter(status=Post.Status.PUBLISHED, category=index_cats[0])[:4]
    second_cat_posts = Post.objects.filter(status=Post.Status.PUBLISHED, category=index_cats[1])[:4]
    third_cat_posts = Post.objects.filter(status=Post.Status.PUBLISHED, category=index_cats[2])[:4]
    context = {
        'posts': posts,
        'index_cats': index_cats,
        'first_cat_posts': first_cat_posts,
        'second_cat_posts': second_cat_posts,
        'third_cat_posts': third_cat_posts
    }
    return render(request, 'post/index.html', context)


def post_detail(request, id):
    try:
        post = Post.objects.get(status=Post.Status.PUBLISHED, pk=id)
    except Post.DoesNotExist:
        raise Http404('Post not found')
    post.views_count = post.views_count + 1
    post.save()
    context = {
        'post': post
    }
    return render(request, 'post/detail.html', context)

def category_detail(request, id):
    try:
        category = Category.objects.get(is_active=True, pk=id)
    except Category.DoesNotExist:
        raise Http404()
    posts = Post.objects.filter(category=category, status=Post.Status.PUBLISHED)
    context = {
        'category': category,
        'posts': posts
    }
    return render(request, 'post/categories.html', context)
