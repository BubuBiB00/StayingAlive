from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

class Exercise(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=400)
    path = models.TextField()
    create_date = models.DateTimeField("date created")
