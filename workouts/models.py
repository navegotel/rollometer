from django.contrib.auth import get_user_model
from django.db import models

class WorkoutType(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return self.name

class Workout(models.Model):
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3
    PRO = 4
    DIFFICULTY_CHOICES = [
        (BEGINNER, 'Beginner'),
        (INTERMEDIATE, 'Intermediate'),
        (ADVANCED, 'Advanced'),
        (PRO, 'Pro/Specific')
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    public = models.BooleanField(default=True)
    workout_type = models.ForeignKey(WorkoutType, on_delete=models.PROTECT)
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=40, unique=True)
    description = models.CharField(max_length=2048)
    difficulty = models.PositiveSmallIntegerField(choices=DIFFICULTY_CHOICES, default=BEGINNER)

    class Meta:
        ordering = ('name', 'difficulty', )

    def __str__(self):
        return self.name


def exercise_gif_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/exercise/{id}.gif
    return 'exercise/{1}.gif'.format(instance.id)


class Exercise(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    gif = models.FileField(upload_to=exercise_gif_path, blank=True, null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises')
    name = models.CharField(max_length=30)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, blank=True, null=True)
    duration = models.PositiveSmallIntegerField()
    pause = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

