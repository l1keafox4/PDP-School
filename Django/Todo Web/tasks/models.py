from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    done = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, default='medium')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    important = models.CharField(max_length=10, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='medium')

    def __str__(self):
        return self.title
