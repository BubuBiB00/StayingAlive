from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .helpers.SFTPConnector import SFTPConnector
from django.template import loader
from .models import Exercise
from django.utils import timezone

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm

from random import randint

# Create your views here.
def index_view(request):
    exercise_list = Exercise.objects.all()
    template = loader.get_template('SAapp/index.html')
    context = { "exercise_list" : exercise_list}
    return HttpResponse(template.render(context, request))
    #output = ", ".join([q.title for q in exercise_list])
    #return HttpResponse(output)


def upload_exercise_view(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        post_data = request.POST
        sftpconnector = SFTPConnector()
        myfile.name = post_data["title"] + ".mp4"

        all_exercises = Exercise.objects.all()
        for exercise in all_exercises:
            if exercise.path == sftpconnector.get_path() + myfile.name:
                print(exercise.description)
                print(exercise.title)
                return render(request, 'SAapp/uploadExercise.html',
                              {
                                  'title_error' : True,
                                  'title' : exercise.title
                              })
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        remote_file_location = sftpconnector.upload_video(filename)
        e = Exercise(title=post_data["title"], description=post_data["description"], path=remote_file_location, create_date=timezone.now())
        e.save()
        fs.delete(myfile.name)
        return render(request, 'SAapp/uploadExercise.html', {
            'uploaded_file_url': remote_file_location
        })
    return render(request, 'SAapp/uploadExercise.html')

def exercise_sequence_view(request):
    sequence_length = 5
    training = []
    exercise_names = []
    template = loader.get_template('SAapp/exercise_sequence.html')

    all_exercises = Exercise.objects.all()
    if len(all_exercises) >= sequence_length:
        while (len(training) < sequence_length):
                index = randint(0,len(all_exercises)-1)
                if all_exercises[index] not in training:
                    training.append(all_exercises[index])
                    exercise_names.append(all_exercises[index].title)
    
    #TODO Correct Error Message if less than 5 exercise in db

    request.session["exercise_sequence_title"] = exercise_names

    context = { "exercise_sequence" : training}
    return HttpResponse(template.render(context, request))


def exercise_list_view(request):
    template = loader.get_template('SAapp/exercise_list.html')
    exercise_list = []

    all_exercises = Exercise.objects.all()

    for exercise in all_exercises:
        exercise_list.append(exercise)

    context = { "exercise_list" : exercise_list}
    return HttpResponse(template.render(context, request))

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'SAapp/auth/login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'SAapp/auth/signup.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

def watch_exercise_view(request, video_name):
    with open("SAapp/helpers/config.txt") as file:
        line = file.readline()
    data = line.split(",")
    username = data[2]
    video_list = request.session["exercise_sequence_title"]
    current_index = video_list.index(video_name.split(".mp4")[0])

    if current_index < 4:
        next_video = video_list[current_index + 1]
    else:
        next_video = None
    return render(request, template_name='SAapp/watchExercise.html', context={ "current_video": video_list[current_index], "next_video": next_video, "user_name":username})


def delete_exercise_view(request):
    exercise_id = int(request.GET.get('exercise_id'))
    exercise_to_delete = Exercise.objects.get(id=exercise_id)
    print(exercise_to_delete.title)
    sftpconnector = SFTPConnector()
    sftpconnector.delete_video(f"{exercise_to_delete.title}.mp4")
    exercise_to_delete.delete()
    return redirect('/exercise_list')

def edit_exercise_view(request):
    exercise_to_edit_id = int(request.GET.get('exercise_id'))
    exercise_to_edit = Exercise.objects.get(id=exercise_to_edit_id)
    if request.method == 'POST':
        post_data = request.POST
        if len(request.FILES) > 0:
            if request.FILES['myfile']:
                myfile = request.FILES['myfile']
                sftpconnector = SFTPConnector()
                sftpconnector.delete_video(f"{exercise_to_edit.title}.mp4")
                fs = FileSystemStorage()
                myfile.name = post_data["title"] + ".mp4"
                fs.save(myfile.name, myfile)
                remote_file_location = sftpconnector.upload_video(myfile.name)
                exercise_to_edit.path = remote_file_location
        exercise_to_edit.title = post_data["title"]
        exercise_to_edit.description = post_data["description"]
        exercise_to_edit.save()
        if len(request.FILES) > 0:
            if request.FILES['myfile']:
                fs.delete(myfile.name)
        return redirect('/exercise_list')

    template = loader.get_template('SAapp/editExercise.html')
    context = { "exercise" : exercise_to_edit, "exercise_name" : exercise_to_edit.path.split("/")[-1]}
    return HttpResponse(template.render(context, request))