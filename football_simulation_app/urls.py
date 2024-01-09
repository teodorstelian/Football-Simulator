from django.urls import path
from .views import team_detail_view, select_team_view, TeamSuggestionsView, \
    select_player_view, player_detail_view, PlayerSuggestionsView, country_detail_view, statistics_view

urlpatterns = [
    # path('new_game/', new_game_view, name='new_game_view'),
    path('select_team/', select_team_view, name='select_team'),
    path('select_player/', select_player_view, name='select_player'),
    path('player_detail/<int:player_id>/', player_detail_view, name='player_detail'),
    path('team/<int:team_id>/', team_detail_view, name='team_detail'),
    path('country/<int:country_id>/', country_detail_view, name='country_detail'),
    path('get_team_suggestions/', TeamSuggestionsView.as_view(), name='get_team_suggestions'),
    path('get_player_suggestions/', PlayerSuggestionsView.as_view(), name='get_player_suggestions'),
    path('statistics/', statistics_view, name='statistics'),
    # path('simulate_cup/', simulate_cup_view, name='simulate_cup_view'),
    path('', select_team_view)
]
