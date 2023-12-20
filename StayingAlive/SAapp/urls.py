from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView, name="index"),
    path("upload/", views.UploadExerciseView, name="upload"),
    path("exercise_sequence/", views.ExerciseSequenceView, name="exercise_sequence")]