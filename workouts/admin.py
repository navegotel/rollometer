import logging
from django.contrib import admin
from .models import Workout, Exercise, WorkoutExercise, WorkoutType

logger = logging.getLogger('console')

admin.site.site_title = "Roll-O-Meter"
admin.site.site_header = "Roll-O-Meter"
admin.site.index_title = "Roll-O-Meter"

class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [WorkoutExerciseInline]

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    pass

@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


@admin.register(WorkoutType)
class WorkoutTypeAdmin(admin.ModelAdmin):
    pass