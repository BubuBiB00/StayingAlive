from asyncio import AbstractServer
from django.conf import settings
from django.db import models

class Exercise(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=400)
    path = models.TextField()
    create_date = models.DateTimeField("date created")

class CustomUser(AbstractServer):
    AUTH_USER_MODEL = 'SAapp.CustomUser'
    username = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    password1 = models.CharField(max_length=64)
    password2 = models.CharField(max_length=64)

    class Meta:
        permissions = (("app.tier_1","limited_access"))
