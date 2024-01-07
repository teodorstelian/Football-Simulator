from django.urls import path
from .views import new_game_view, team_detail_view, select_team_view

urlpatterns = [
    path('new_game/', new_game_view, name='new_game_view'),
    path('team/<str:team_name>/', team_detail_view, name='team_detail'),
    path('select_team/', select_team_view, name='select_team'),
]
