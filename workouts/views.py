from django.shortcuts import render
from .models import Workout, WorkoutExercise, WorkoutType
from django.contrib.auth import get_user_model

def index(request):
    context = {
        'workoutlist': Workout.objects.order_by('name'),
        'workouttypelist': WorkoutType.objects.order_by('name'),
        'workoutdifficultylist': Workout.DIFFICULTY_CHOICES,
        'userlist': get_user_model().objects.order_by('last_name')
    }
    return render(request, 'workouts/index.html', context)

def workout(request, slug):
    context = {
        'workout': Workout.objects.get(slug__exact=slug)
    }
    return render(request, 'workouts/workouttimer.html', context)
