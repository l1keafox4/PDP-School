from django.db import models

class Category(models.Model):
    title = models.CharField(max_length=255)

    objects = models.Manager()

class Post(models.Model):
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
