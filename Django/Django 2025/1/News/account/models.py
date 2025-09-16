from django.db import models

# Create your models here.
class Users(models.Model):
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    subject = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name}"
    
class Profile(models.Model):
    user = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    bio = models.TextField()
    location = models.CharField(max_length=255)


    def __str__(self):  
        return f"{self.user}"