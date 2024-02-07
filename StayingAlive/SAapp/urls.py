from django.urls import path

from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("upload/", views.upload_exercise_view, name="upload"),
    path("exercise_sequence/", views.exercise_sequence_view, name="exercise_sequence"),
    path("exercise_list/", views.exercise_list_view, name="exercise_list"),
    path("watch/", views.watch_exercise_view, name="watch"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),]
