from django.shortcuts import render, get_object_or_404, redirect

from football_simulation_app.forms import TeamSelectionForm
from football_simulation_app.models import Team
from src.main import MainProgram


# Create your views here.

def team_detail_view(request, team_name):
    team = get_object_or_404(Team, name=team_name)
    return render(request, 'team_detail.html', {'team': team})

def select_team_view(request):
    if request.method == 'POST':
        form = TeamSelectionForm(request.POST)
        if form.is_valid():
            team_name = form.cleaned_data['team_name']
            return redirect('team_detail', team_name=team_name)
    else:
        form = TeamSelectionForm()

    return render(request, 'select_team.html', {'form': form})

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