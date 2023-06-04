from database import get_best_teams
from leagues import simulate_season, select_league

while True:
    print("1. Simulate a league \n"
          "2. Check best teams")
    action = input("Select action: ")

    league, league_teams = select_league()
    if action == "1":
        simulate_season(league, league_teams)
    if action == "2":
        get_best_teams(league)

