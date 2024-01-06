from django.shortcuts import render

from src.main import MainProgram


# Create your views here.
def simulation_view(request):
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