from django.urls import path
from .views import get_workouts, create_workout

urlpatterns = [
    path("", get_workouts, name="get_workouts"),
    path("create", create_workout, name="create_workout"),
]