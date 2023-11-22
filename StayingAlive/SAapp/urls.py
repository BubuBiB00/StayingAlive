from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView, name="index"),
    path("upload/", views.upload_exercise, name="upload")]
