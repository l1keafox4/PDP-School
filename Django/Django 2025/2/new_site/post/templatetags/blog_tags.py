from django import template
from ..models import *

register = template.Library()

@register.simple_tag
def get_categories():
    return Category.objects.filter(is_active=True)

@register.simple_tag
def get_popular_posts():
    return Post.objects.filter(status=Post.Status.PUBLISHED).order_by('-views_count')[:4]

@register.simple_tag
def get_recent_posts():
    return Post.objects.filter(status=Post.Status.PUBLISHED).order_by('-published_date')[:4]

