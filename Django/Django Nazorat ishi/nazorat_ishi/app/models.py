from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=255)
    work = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return self.name
