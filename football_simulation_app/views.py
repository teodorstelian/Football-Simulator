from django.db.models import Q, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from football_simulation_app.forms import TeamSelectionForm, SelectPlayerForm, LineupForm
from football_simulation_app.models import Team, Player, Country, Statistics
from football_simulation_project.settings import POSITION_THRESHOLD, FORMATION_4_4_2


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

    # Fetch statistics for the player
    player_statistics = Statistics.objects.filter(player=player)

    # Calculate total statistics
    total_apps = player_statistics.aggregate(total_apps=Sum('apps'))['total_apps'] or 0
    total_goals = player_statistics.aggregate(total_goals=Sum('goals'))['total_goals'] or 0
    total_assists = player_statistics.aggregate(total_assists=Sum('assists'))['total_assists'] or 0

    # Group statistics by club
    club_statistics = player_statistics.values('team__name').annotate(
        total_apps=Sum('apps'),
        total_goals=Sum('goals'),
        total_assists=Sum('assists')
    )

    # Group statistics by position
    position_statistics = player_statistics.values('position').annotate(
        total_apps=Sum('apps'),
        total_goals=Sum('goals'),
        total_assists=Sum('assists')
    )

    return render(request, 'player_detail.html', {
        'player': player,
        'total_apps': total_apps,
        'total_goals': total_goals,
        'total_assists': total_assists,
        'club_statistics': club_statistics,
        'position_statistics': position_statistics,
    })

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

# def new_game_view(request):
#     program = MainProgram()
#
#     if request.method == 'POST':
#         choice = request.POST.get('choice')
#
#         if choice == "simulate_season":
#             program.simulate_season()
#         elif choice == "simulate_league":
#             program.simulate_league()
#         elif choice == "simulate_cup":
#             program.simulate_cup()
#         elif choice == "simulate_european":
#             program.simulate_european()
#         elif choice == "get_best_teams":
#             result = program.get_best_teams(program.league)
#             return render(request, 'main.html', {'result': result})
#         elif choice == "check_team_stats":
#             input_team = request.POST.get('team_name')
#             result = program.check_team_stats(input_team)
#             return render(request, 'main.html', {'result': result})
#
#     return render(request, 'main.html')


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

    if request.method == 'POST':
        form = LineupForm(request.POST)
        if form.is_valid():

            team_id = form.cleaned_data['team']
            positions = FORMATION_4_4_2
            for pos in positions:
                current_pos_id = form.cleaned_data[pos]
                if pos in ["CB1", "CB2"]:
                    pos = "CB"
                elif pos in ["CDM1", "CDM2"]:
                    pos = "CDM"

                # Check if the Statistics object already exists for the player and position
                existing_stats = Statistics.objects.filter(player_id=current_pos_id, team_id=team_id,
                                                           position=pos).first()

                if existing_stats:
                    existing_stats.apps += 1
                    existing_stats.save()
                else:
                    Statistics.objects.create(player_id=current_pos_id, team_id=team_id, position=pos, apps=1, goals=0, assists=0,
                                          yellow_cards=0, red_cards=0, season="2023/24")

            return JsonResponse({'message': 'Lineup submitted successfully'})
        else:
            errors = {field: form.errors[field][0] for field in form.errors}
            return JsonResponse({'message': 'Invalid form submission', 'errors': errors})
    else:
        form = LineupForm()

    context = {'countries': countries, 'form': form}
    return render(request, 'select_lineup.html', context)

def ajax_get_teams_and_players(request):
    if request.method == 'GET':
        country_id = request.GET.get('country_id')
        team_id = request.GET.get('team_id')

        if country_id:
            teams = Team.objects.filter(country=country_id).values('id', 'name')
            return JsonResponse({'teams': list(teams)})

        elif team_id:
            gk = Player.objects.filter(team=team_id, GK__gt = POSITION_THRESHOLD).values('id', 'name', 'GK')
            lb = Player.objects.filter(team=team_id, LB__gt = POSITION_THRESHOLD).values('id', 'name', 'LB')
            cb = Player.objects.filter(team=team_id, CB__gt = POSITION_THRESHOLD).values('id', 'name', 'CB')
            rb = Player.objects.filter(team=team_id, RB__gt = POSITION_THRESHOLD).values('id', 'name', 'RB')
            cdm = Player.objects.filter(team=team_id, CDM__gt = POSITION_THRESHOLD).values('id', 'name', 'CDM')
            cam = Player.objects.filter(team=team_id, CAM__gt = POSITION_THRESHOLD).values('id', 'name', 'CAM')
            lw = Player.objects.filter(team=team_id, LW__gt = POSITION_THRESHOLD).values('id', 'name', 'LW')
            rw = Player.objects.filter(team=team_id, RW__gt = POSITION_THRESHOLD).values('id', 'name', 'RW')
            st = Player.objects.filter(team=team_id, ST__gt = POSITION_THRESHOLD).values('id', 'name', 'ST')
            return JsonResponse({'GK': list(gk),
                                 'LB': list(lb),
                                 'CB': list(cb),
                                 'RB': list(rb),
                                 'CDM': list(cdm),
                                 'CAM': list(cam),
                                 'LW': list(lw),
                                 'RW': list(rw),
                                 'ST': list(st)},
                                )

    return JsonResponse({'error': 'Invalid request'})