from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('workout/<slug:slug>/', views.workout, name='workout')
]
