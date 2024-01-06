# urls.py

from django.urls import path
from .views import simulation_view

urlpatterns = [
    path('simulate/', simulation_view, name='simulation_view'),
]
