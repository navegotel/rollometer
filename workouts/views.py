from django.shortcuts import render
from .models import Workout, WorkoutExercise, WorkoutType
from django.contrib.auth import get_user_model

def index(request):
    context = {
        'selectedworkouttypes': [ int(x) for x in request.GET.getlist('workouttype')],
        'selectedworkoutdifficulties': [ int(x) for x in request.GET.getlist('workoutdifficulty')],
        'selectedusers': [ int(x) for x in request.GET.getlist('user')],
        'workouttypelist': WorkoutType.objects.order_by('name'),
        'workoutdifficultylist': Workout.DIFFICULTY_CHOICES,
        'userlist': get_user_model().objects.order_by('last_name')
    }
    query_set = Workout.objects.order_by('name')
    if len(context['selectedworkouttypes']) > 0:
        query_set = query_set.filter(workout_type__in=context['selectedworkouttypes'])
    if len(context['selectedworkoutdifficulties']) > 0:
        query_set = query_set.filter(difficulty__in=context['selectedworkoutdifficulties'])
    if len(context['selectedusers']) > 0:
        query_set = query_set.filter(user__in=context['selectedusers'])
        
    context['workoutlist'] = query_set
    return render(request, 'workouts/index.html', context)

def workout(request, slug):
    context = {
        'workout': Workout.objects.get(slug__exact=slug)
    }
    return render(request, 'workouts/workouttimer.html', context)
