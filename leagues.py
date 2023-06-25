import matches
import settings
from team import Team
from database import create_teams_table, get_teams, update_team


def select_league():
    """
        Method used to select which league to use. Creates the league table if it doesn't exist.
    :return:
    """
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
    create_teams_table(country) # Create the league table if it doesn't exist
    teams_obj = get_teams(country)
    # Checks if the database is empty
    if len(teams_obj) == 0:
        # Get original teams from settings
        teams_obj, teams_name = get_default_teams_country(teams, country)
    else:
        teams_name = [team.name for team in teams_obj]

    if country is None or teams_obj is None or teams_name is None:
        raise ValueError("Invalid value")

    print(f"Selected league: {league}")
    print(f"Country: {country}")
    print(f"Teams: {teams_name}")

    return country, teams_obj, teams_name

def simulate_season(league, teams_obj):
    """
        Simulate a league by playing th efixtures, updating the teams and generating the standings
    :param league:
    :param teams_obj:
    :return:
    """
    matches.play_fixture_league(teams_obj)

    for team in teams_obj:
        update_team(team, league)  # Update team data in the database

    teams = get_teams(league)  # Retrieve teams with updated data from the database
    return matches.generate_standings(teams, league)

def get_default_teams_country(teams, country):
    """
        Generate the teams found in the settings
    :param teams: The default teams from settings
    :param country: The country we want to add the default teams
    :return: The teams as objects and the name of them
    """
    all_teams_obj = []
    all_teams_names = []
    for team, skill in teams:
        new_team = Team(name=team, country=country, skill=skill)
        all_teams_obj.append(new_team)
        all_teams_names.append(new_team.name)
    return all_teams_obj, all_teams_names