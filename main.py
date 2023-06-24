from database import get_best_teams, update_general_table, create_general_table, generate_teams_table
from leagues import simulate_season, select_league

while True:
    print("1. Simulate a league \n"
          "2. Check best teams \n"
          "3. See stats for a team")
    action = input("Select action: ")

    league, teams_obj, teams_name = select_league()
    generate_teams_table(league, teams_obj)
    create_general_table()
    for team in teams_obj:
        update_general_table(team)
    if action == "1":
        teams_obj = simulate_season(league, teams_obj)
        for team in teams_obj:
            update_general_table(team)
    if action == "2":
        get_best_teams(league)
    if action == "3":
        input_team = input("Select team: ")
        for team in teams_obj:
            if input_team == team.name:
                update_general_table(team)
