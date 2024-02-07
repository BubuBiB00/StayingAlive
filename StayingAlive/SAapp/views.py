from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .helpers.SFTPConnector import SFTPConnector
from django.template import loader
from .models import Exercise
from django.utils import timezone

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout 


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
    template = loader.get_template('SAapp/exercise_sequence.html')

    all_exercises = Exercise.objects.all()

    while (len(training) < sequence_length):
            index = randint(0,len(all_exercises)-1)
            training.append(all_exercises[index])

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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username,password)
        if user is not None:
            login(request, user)
        else:
            pass
    
    else:
        return render(request, 'SAapp/auth/login.html')

def signup_view(request):

    return render(request, 'SAapp/auth/signup.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def watch_exercise_view(request, video_name):
    return render(request, template_name='SAapp/watchExercise.html', context={"video_to_watch":video_name})

