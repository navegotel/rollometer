from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.utils.text import slugify
from django.db.models import Q
from .models import Workout, WorkoutExercise, WorkoutType
from .forms import WorkoutForm, exercise_form_widgets



def index(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            logout(request)
        else:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
    context = {
        'selectedworkouttypes': [ int(x) for x in request.GET.getlist('workouttype')],
        'selectedworkoutdifficulties': [ int(x) for x in request.GET.getlist('workoutdifficulty')],
        'selectedusers': [ int(x) for x in request.GET.getlist('user')],
        'workouttypelist': WorkoutType.objects.order_by('name'),
        'workoutdifficultylist': Workout.DIFFICULTY_CHOICES,
        'userlist': get_user_model().objects.order_by('last_name')
    }

    if request.user.is_authenticated:
        query_set = Workout.objects.filter(Q(user=request.user) | Q(public=True)).order_by('name')
    else: 
        query_set = Workout.objects.filter(public=True).order_by('name')
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


def edit_workout(request, slug):
    workout = Workout.objects.get(slug__exact=slug)
    ExerciseFormset = inlineformset_factory(Workout, WorkoutExercise, fields=('name', 'exercise', 'duration', 'pause'), widgets=exercise_form_widgets)
    if request.method == 'GET':
        mainform =  WorkoutForm(instance=workout)
        exercise_formset = ExerciseFormset(instance=workout)
        context = {'form': mainform, 'formset': exercise_formset}
        return render(request, 'workouts/editworkout.html', context)   
    elif request.method == 'POST':
        mainform = WorkoutForm(request.POST, instance=workout)
        if mainform.is_valid():
            workout.save()
        exercise_formset = ExerciseFormset(request.POST, instance=workout)
        if exercise_formset.is_valid():
            exercise_formset.save()
            return HttpResponseRedirect(reverse('index'))
        else:
            context = {'form': mainform, 'formset': exercise_formset}
            return render(request, 'workouts/editworkout.html', context)

def add_workout(request):
    if request.method == 'POST':
        form =  WorkoutForm(request.POST)
        if form.is_valid():
            slug = "{0}-{1}".format(request.user.username, slugify(request.POST.get('name')))[:30]
            workout = Workout(user=request.user, public=form.cleaned_data['public'], 
                              workout_type=form.cleaned_data['workout_type'], name=form.cleaned_data['name'],
                              slug=slug, description=form.cleaned_data['description'], 
                              difficulty=form.cleaned_data['difficulty']
                              )
            workout.save()
            return HttpResponseRedirect(reverse('editworkout', kwargs={'slug':slug}))
    else:
        form = WorkoutForm(initial={'user':request.user, 'slug':'new-workout'})
    context = {'form': form}
    return render(request, 'workouts/addworkout.html', context)

