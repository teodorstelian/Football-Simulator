import settings

import matches
from database import create_teams_table, get_teams, update_team, insert_team
from classes import Team
from teams import teams_england, teams_spain, teams_germany, teams_italy, teams_france


def select_league():
    print("1. Premier League (England) \n"
          "2. La Liga (Spain) \n"
          "3. Bundesliga (Germany) \n"
          "4. Ligue 1 (France) \n"
          "5. Serie A (Italy)")

    league_mapping = {
        '1': (settings.ENG, teams_england()[0], teams_england()[1]),
        '2': (settings.ESP, teams_spain()[0], teams_spain()[1]),
        '3': (settings.GER, teams_germany()[0], teams_germany()[1]),
        '4': (settings.FRA, teams_france()[0], teams_france()[1]),
        '5': (settings.ITA, teams_italy()[0], teams_italy()[1]),
    }

    league = input("Enter the league number: ")
    country, teams_obj, teams_name = league_mapping.get(league, (None, None, None))

    if country is None or teams_obj is None or teams_name is None:
        raise ValueError("Invalid value")

    print(f"Selected league: {league}")
    print(f"Country: {country}")
    print(f"Teams: {teams_name}")

    return country, teams_obj, teams_name


def generate_teams(teams, league):
    for team in teams:
        insert_team(team, league)  # Insert teams into the database

    return teams


def generate_teams_table(league, teams_obj):
    create_teams_table(league)  # Create the teams table if it doesn't exist

    cur_teams = get_teams(league)  # Retrieve teams from the database

    if len(cur_teams) == 0:
        cur_teams = generate_teams(teams_obj, league)

    return cur_teams


def simulate_season(league, teams_obj):
    cur_teams = generate_teams_table(league, teams_obj)
    matches.play_fixture(cur_teams)

    for team in cur_teams:
        update_team(team, league)  # Update team data in the database

    teams = get_teams(league)  # Retrieve teams with updated data from the database
    matches.generate_standings(teams)
