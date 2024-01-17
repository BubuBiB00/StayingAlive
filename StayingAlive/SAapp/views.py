import os

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .helpers.SFTPConnector import SFTPConnector
from .models import Exercise
from django.utils import timezone
from os import listdir


# Create your views here.
def IndexView(request):
    exercise_list = Exercise.objects.all()
    print(exercise_list.count())
    #output = exercise_list[0].title + exercise_list[0].path
    output = ", ".join([q.title + q.path for q in exercise_list])
    return HttpResponse(output)

def upload_exercise(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        sftpconnector = SFTPConnector()

        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        remote_file_location = sftpconnector.upload_video(myfile.name)
        e = Exercise(title=myfile.name, description="", path=remote_file_location, create_date=timezone.now())
        e.save()
        fs.delete(myfile.name)
        return render(request, 'SAapp/uploadExercise.html', {
            'uploaded_file_url': remote_file_location
        })
    return render(request, 'SAapp/uploadExercise.html')

def watch_exercise(request):
    clear_folder()
    video_name = ""
    ftpconnector = SFTPConnector()
    try:
        ftpconnector.get_video(f"home/sebastian.karner/StayingAlive/{video_name}")
    except Exception as e:
        print(e)
        return HttpResponseNotFound("<h1>This Exercise is not available!</h1>")
    return render(request, template_name='SAapp/watchExercise.html', context={"video_to_watch":video_name})

def clear_folder():
    for i in listdir(f"SAapp\\media\\"):
        os.remove(f"SAapp\\media\\{i}")
