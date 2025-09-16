from django.shortcuts import render
from post.models import Post

def news_view(request):
    dataset = Post.objects.all()
    return render(request, "news.html", {"dataset": dataset})
