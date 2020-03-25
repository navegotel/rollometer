from django.shortcuts import render
from .models import Workout, WorkoutExercise

def index(request):
    context = {
        'workoutlist': Workout.objects.order_by('name')
    }
    return render(request, 'workouts/index.html', context)

def workout(request, slug):
    context = {
        'workout': Workout.objects.get(slug__exact=slug)
    }
    return render(request, 'workouts/workouttimer.html', context)
