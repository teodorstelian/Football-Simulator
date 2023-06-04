import settings

import matches
from database import create_teams_table, get_teams, update_team, insert_team
from teams import Team


def select_league():
    print("1. Premier League (England) \n"
          "2. La Liga (Spain) \n"
          "3. Bundesliga (Germany) \n"
          "4. Ligue 1 (France) \n"
          "5. Serie A (Italy)")

    league_mapping = {
        '1': (settings.ENG, settings.ENG_TEAMS),
        '2': (settings.ESP, settings.ESP_TEAMS),
        '3': (settings.GER, settings.GER_TEAMS),
        '4': (settings.FRA, settings.FRA_TEAMS),
        '5': (settings.ITA, settings.ITA_TEAMS),
    }

    league = input("Enter the league number: ")
    country, teams = league_mapping.get(league, (None, None))

    if country is None or teams is None:
        raise ValueError("Invalid value")

    print(f"Selected league: {league}")
    print(f"Country: {country}")
    print(f"Teams: {teams}")

    return country, teams


def generate_teams(country_teams, league):
    teams = [Team(_) for _ in country_teams]
    for team in teams:
        insert_team(team, league)  # Insert teams into the database

    return teams


def simulate_season(league, league_teams):

    create_teams_table(league)  # Create the teams table if it doesn't exist

    cur_teams = get_teams(league)  # Retrieve teams from the database

    if len(cur_teams) == 0:
        cur_teams = generate_teams(league_teams, league)

    matches.generate_fixtures(cur_teams)

    for team in cur_teams:
        update_team(team, league)  # Update team data in the database

    teams = get_teams(league)  # Retrieve teams with updated data from the database
    matches.generate_standings(teams)
