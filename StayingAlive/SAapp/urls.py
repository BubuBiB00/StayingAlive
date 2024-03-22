from django.urls import include, path

from . import views

urlpatterns = [
    path("", views.index_view, name="index"),
    path("watch/<str:video_name>", views.watch_exercise_view, name="watch"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.user_logout, name="logout"),
    path("delete_exercise/",views.delete_exercise_view, name="delete_exercise"),
    path("edit_exercise/",views.edit_exercise_view, name="edit_exercise"),

    path("upload/", views.upload_exercise_view, name="upload"),
    path("exercise_sequence/", views.exercise_sequence_view, name="exercise_sequence"),
    path("exercise_list/", views.exercise_list_view, name="exercise_list"),
    
    path('microsoft/', include('microsoft_auth.urls', namespace='microsoft')),]
