from django.db import models

class Exercise(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=400)
    path = models.TextField()
    create_date = models.DateTimeField("date created")
