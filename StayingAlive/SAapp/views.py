import os

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .helpers.SFTPConnector import SFTPConnector
from django.template import loader
from .models import Exercise
from django.utils import timezone
from os import listdir

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 
from .forms import UserCreationForm, LoginForm

from random import randint

# Create your views here.
def IndexView(request):
    exercise_list = Exercise.objects.all()
    template = loader.get_template('SAapp/index.html')
    context = { "exercise_list" : exercise_list}
    return HttpResponse(template.render(context, request))
    #output = ", ".join([q.title for q in exercise_list])
    #return HttpResponse(output)

def UploadExerciseView(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        post_data = request.POST
        sftpconnector = SFTPConnector()

        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        remote_file_location = sftpconnector.upload_video(myfile.name)
        e = Exercise(title=post_data["title"], description=post_data["description"], path=remote_file_location, create_date=timezone.now())
        e.save()
        fs.delete(myfile.name)
        return render(request, 'SAapp/uploadExercise.html', {
            'uploaded_file_url': remote_file_location
        })
    return render(request, 'SAapp/uploadExercise.html')

def ExerciseSequenceView(request):
    sequence_length = 5
    training = []
    template = loader.get_template('SAapp/exercise_sequence.html')

    all_exercises = Exercise.objects.all()

    while (len(training) < sequence_length):
            index = randint(0,len(all_exercises)-1)
            training.append(all_exercises[index])

    context = { "exercise_sequence" : training}
    return HttpResponse(template.render(context, request))

def ExerciseListView(request):
    template = loader.get_template('SAapp/exercise_list.html')
    exercise_list = []

    all_exercises = Exercise.objects.all()

    for exercise in all_exercises:
        exercise_list.append(exercise)

    context = { "exercise_list" : exercise_list}
    return HttpResponse(template.render(context, request))

def LoginView(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'SAapp/login.html', {'form': form})

def SignupView(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'SAapp/signup.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

def watch_exercise_view(request):
    video_name = "sample-5s.mp4"
    return render(request, template_name='SAapp/watchExercise.html', context={"video_to_watch":video_name})
