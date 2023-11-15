from django.http import HttpResponse

from .models import Exercise


# Create your views here.
def IndexView(request):
    exercise_list = Exercise.objects.all()
    output = ", ".join([q.title for q in exercise_list])
    return HttpResponse(output)