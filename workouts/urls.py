from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('workout/edit/<slug:slug>/', views.edit_workout, name='editworkout'),
    path('workout/add/', views.add_workout, name='addworkout'),
    path('workout/<slug:slug>/', views.workout, name='workout')
]
