from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView, name="index"),
    path("upload/", views.UploadExerciseView, name="upload"),
    path("exercise_sequence/", views.ExerciseSequenceView, name="exercise_sequence"),
    path("exercise_list/", views.ExerciseListView, name="exercise_list"),
    path("watch/", views.watch_exercise_view, name="watch"),
    path("login/", views.LoginView, name="login"),
    path("signup/", views.SignupView, name="signup"),
    path("loggedin/",views.logged_in_view, name="loggedin"),
    path("delete_exercise/",views.delete_exercise_view, name="delete_exercise"),
    path("edit_exercise/",views.edit_exercise_view, name="edit_exercise")]

