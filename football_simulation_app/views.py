from django.db.models import Q
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from football_simulation_app.forms import TeamSelectionForm, SelectPlayerForm
from football_simulation_app.models import Team, Player
from src.leagues import cup_simulation
from src.main import MainProgram

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


def simulate_cup_view(request):
    league_name = "YourLeagueName"  # Replace with your actual league name
    num_teams_to_select = 8  # Adjust the number of top teams you want to select

    teams = Team.objects.filter(country=league_name).order_by('-skill')[:num_teams_to_select]

    if request.method == 'POST':
        # Run cup simulation
        teams = cup_simulation(league_name, teams)

        # Update teams in the database
        for team in teams:
            team.save()

        # Redirect to the same page to avoid form resubmission on page reload
        return HttpResponseRedirect(reverse('simulate_cup_view'))

    context = {
        'teams': teams,
    }

    return render(request, 'simulate_cup.html', context)

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