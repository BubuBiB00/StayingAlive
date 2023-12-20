from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from .helpers.SFTPConnector import SFTPConnector
from django.template import loader
from .models import Exercise
from django.utils import timezone

from random import randint

# Create your views here.
def IndexView(request):
    exercise_list = Exercise.objects.all()
    template = loader.get_template('SAapp/index.html')
    context = { "exercise_list" : exercise_list}
    return HttpResponse(template.render(context, request))
    #output = ", ".join([q.title for q in exercise_list])
    #return HttpResponse(output)

#Show exercise view.
def ExerciseView(request):
    exercis_sequence_list = Exercise.objects.all()
    template = loader.get_template('SAapp/exercise.html')
    context = { "exercis_sequence_list" : exercis_sequence_list}
    return HttpResponse(template.render(context, request))

def upload_exercise(request):
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

def exercise_sequence(request):
    sequence_length = 5
    training = []
    template = loader.get_template('SAapp/exercise.html')

    all_exercises = Exercise.objects.all()

    for i in range(sequence_length):
        index = randint(0,len(all_exercises)-1)
        training.append(all_exercises[index])

    context = { "exercise_sequence_list" : training}
    return HttpResponse(template.render(context, request))