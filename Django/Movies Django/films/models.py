from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Movie(models.Model):
    title = models.CharField(
        max_length=200,
        blank=False,
        null=False
    )
    description = models.TextField(
        blank=False,
        null=False
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        blank=False,
        null=False
    )

    def __str__(self):
        return self.title
