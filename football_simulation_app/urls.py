from django.urls import path
from .views import new_game_view, team_detail_view, select_team_view, TeamSuggestionsView, simulate_cup_view, \
    select_player_view, player_detail_view, PlayerSuggestionsView

urlpatterns = [
    path('new_game/', new_game_view, name='new_game_view'),
    path('team/<int:team_id>/', team_detail_view, name='team_detail'),
    path('select_team/', select_team_view, name='select_team'),
    path('select_player/', select_player_view, name='select_player'),
    path('player_detail/<int:player_id>/', player_detail_view, name='player_detail'),
    path('get_team_suggestions/', TeamSuggestionsView.as_view(), name='get_team_suggestions'),
    path('get_player_suggestions/', PlayerSuggestionsView.as_view(), name='get_player_suggestions'),
    path('simulate_cup/', simulate_cup_view, name='simulate_cup_view'),
]
