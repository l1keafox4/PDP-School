from django.db import models

# Create your models here.

class Contact(models.Model):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=100, default="USA")
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    def __str__(self):
        return f"{self.first_name}"
    
class Info(models.Model):
    title = models.CharField(max_length=255)
    instagram = models.CharField(max_length=255)
    telegram = models.CharField(max_length=255)
    tiktok = models.CharField(max_length=255)
    websites = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, null=True, blank=True)


    def __str__(self):
        return f"{self.title}"
