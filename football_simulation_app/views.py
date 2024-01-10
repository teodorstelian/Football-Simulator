from django.db.models import Q
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from football_simulation_app.forms import TeamSelectionForm, SelectPlayerForm
from football_simulation_app.models import Team, Player, Country
from src.initial_data import POSITIONS
from src.leagues import cup_simulation
from src.main import MainProgram

def country_detail_view(request, country_id):
    country = get_object_or_404(Country, id=country_id)
    players = Player.objects.filter(country=country)

    context = {'country': country, 'players': players}
    return render(request, 'country_detail.html', context)

def team_detail_view(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    players = Player.objects.filter(team=team)

    context = {'team': team, 'players': players}
    return render(request, 'team_detail.html', context)

def player_detail_view(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    return render(request, 'player_detail.html', {'player': player})

def select_team_view(request):
    if request.method == 'POST':
        form = TeamSelectionForm(request.POST)
        if form.is_valid():
            team_name = form.cleaned_data['team_name']
            team_id = get_object_or_404(Team, name=team_name).id
            return redirect('team_detail', team_id=team_id)
    else:
        form = TeamSelectionForm()

    return render(request, 'select_team.html', {'form': form})


def select_player_view(request):
    if request.method == 'POST':
        form = SelectPlayerForm(request.POST)
        if form.is_valid():
            player_name = form.cleaned_data['player_name']
            player_id = get_object_or_404(Player, name=player_name).id
            return redirect('player_detail', player_id=player_id)
    else:
        form = SelectPlayerForm()

    return render(request, 'select_player.html', {'form': form})

def new_game_view(request):
    program = MainProgram()

    if request.method == 'POST':
        choice = request.POST.get('choice')

        if choice == "simulate_season":
            program.simulate_season()
        elif choice == "simulate_league":
            program.simulate_league()
        elif choice == "simulate_cup":
            program.simulate_cup()
        elif choice == "simulate_european":
            program.simulate_european()
        elif choice == "get_best_teams":
            result = program.get_best_teams(program.league)
            return render(request, 'main.html', {'result': result})
        elif choice == "check_team_stats":
            input_team = request.POST.get('team_name')
            result = program.check_team_stats(input_team)
            return render(request, 'main.html', {'result': result})

    return render(request, 'main.html')


# def simulate_cup_view(request):
#     league_name = 1 # Replace with your actual league name
#     num_teams_to_select = 8  # Adjust the number of top teams you want to select
#
#     teams = Team.objects.filter(country=league_name).order_by('-skill')[:num_teams_to_select]
#
#     if request.method == 'POST':
#         # Run cup simulation
#         teams = cup_simulation(league_name, teams)
#
#         # Update teams in the database
#         for team in teams:
#             team.save()
#
#         # Redirect to the same page to avoid form resubmission on page reload
#         return HttpResponseRedirect(reverse('simulate_cup_view'))
#
#     context = {
#         'teams': teams,
#     }
#
#     return render(request, 'simulate_cup.html', context)

class TeamSuggestionsView(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query', '')
        team_suggestions = Team.objects.filter(Q(name__icontains=query))

        suggestions = [{'name': team.name} for team in team_suggestions]
        return JsonResponse(suggestions, safe=False)

class PlayerSuggestionsView(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query', '')
        player_suggestions = Player.objects.filter(Q(name__icontains=query))

        suggestions = [{'name': player.name} for player in player_suggestions]
        return JsonResponse(suggestions, safe=False)

def statistics_view(request):
    # Retrieve the top 10 teams by skill in descending order
    top_teams = Team.objects.order_by('-skill')[:10]
    top_players = Player.objects.order_by('-skill')[:10]
    context = {'top_teams': top_teams, 'top_players': top_players}
    return render(request, 'statistics.html', context)


def select_lineup(request):
    countries = Country.objects.all()
    teams = Team.objects.none()
    players = Player.objects.none()
    context = {'countries': countries, 'teams': teams, 'players': players}
    return render(request, 'select_lineup.html', context)

def ajax_get_teams_and_players(request):
    if request.method == 'GET':
        country_id = request.GET.get('country_id')
        team_id = request.GET.get('team_id')
        if country_id or team_id:
            teams = Team.objects.filter(country=country_id).values('id', 'name')
            players = Player.objects.filter(team=team_id).values('id', 'name', 'GK', 'LB', 'CB', 'RB')

            return JsonResponse({'teams': list(teams), 'players': list(players)})

    return JsonResponse({'error': 'Invalid request'})