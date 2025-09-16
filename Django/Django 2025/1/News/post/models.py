from django.db import models

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    body = models.TextField()
    image =  models.ImageField(upload_to="images/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.author}"
class Category(models.Model):
    name = models.CharField(max_length=70)
    slug = models.SlugField(max_length=70)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}"
