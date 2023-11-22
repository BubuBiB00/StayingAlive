from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .helpers.SFTPConnector import SFTPConnector
from .models import Exercise
from django.utils import timezone


# Create your views here.
def IndexView(request):
    exercise_list = Exercise.objects.all()
    output = ", ".join([q.title for q in exercise_list])
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