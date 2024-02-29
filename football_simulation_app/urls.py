from django.urls import path
from django.views.generic import TemplateView

from . import views
from .views import team_detail_view, TeamSuggestionsView, player_detail_view, \
    PlayerSuggestionsView, country_detail_view, statistics_view, select_lineup, search_view, new_game_view, \
    team_manager_view

urlpatterns = [
    path('', search_view),
    path('search/', search_view, name='search'),
    path('player_detail/<int:player_id>/', player_detail_view, name='player_detail'),
    path('team/<int:team_id>/', team_detail_view, name='team_detail'),
    path('country/<int:country_id>/', country_detail_view, name='country_detail'),

    path('statistics/', statistics_view, name='statistics'),
    path('select_lineups/', select_lineup, name='select_lineups'),

    # Ajax Views
    path('ajax_get_teams_and_players/', views.ajax_get_teams_and_players, name='ajax_get_teams_and_players'),
    path('ajax_get_team_suggestions/', TeamSuggestionsView.as_view(), name='ajax_get_team_suggestions'),
    path('ajax_get_player_suggestions/', PlayerSuggestionsView.as_view(), name='ajax_get_player_suggestions'),

    path('new_game/', new_game_view, name='new_game'),
    path('team-manager/', team_manager_view, name='team_manager'),

]
