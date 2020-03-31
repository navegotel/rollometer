from django.forms import ModelForm, TextInput, HiddenInput, Textarea, Select, CheckboxInput
from .models import Workout, WorkoutExercise

exercise_form_widgets = {'name': TextInput(attrs={'class': 'form-control'}), 
                         'exercise': Select(attrs={'class': 'form-control'}), 
                         'duration': TextInput(attrs={'class': 'form-control', 'type': 'number'}),
                         'pause': TextInput(attrs={'class': 'form-control', 'type': 'number'})
                         }

class WorkoutForm(ModelForm):
    class Meta:
        model = Workout
        # fields = ['slug', 'public', 'name', 'workout_type', 'difficulty', 'description']
        fields = '__all__'
        widgets = {
            'user': HiddenInput(),
            'slug': HiddenInput(),
            'public': CheckboxInput(attrs={'class': 'form-check-input'}),
            'description': Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'workout_type': Select(attrs={'class':'form-control'}),
            'difficulty': Select(attrs={'class':'form-control'}),
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter workout name', 'aria-describedby': 'nameHelp'})
        }

    