from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView, name="index"),
    path("exercise/", views.ExerciseView, name="exercise"),
    path("upload/", views.upload_exercise, name="upload")]
