from django.db import models

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    is_index = models.BooleanField(default=False)
    parent = models.ForeignKey('self', 
                               on_delete=models.PROTECT, 
                               related_name='childs', 
                               blank=True, 
                               null=True)

    def __str__(self):
        return self.name
    

class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,unique_for_date='published_date')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')
    photo = models.ImageField(upload_to='posts/',)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,    
                               related_name='blog_posts',)
    body = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                                 choices=Status.choices,
                                 default=Status.PUBLISHED)
    views_count = models.IntegerField(default=0)


    class Meta:
        ordering = ['-published_date']
        indexes = [
            models.Index(fields=['-published_date']),
        ]



    def __str__(self):
        return self.title

    

    
