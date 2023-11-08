from django.db import models

class Exercise(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=400)
    path = models.TextField()
    create_date = models.DateTimeField("date created")
