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
          "5. Serie A (Italy) \n"
          "6. Eredivisie (Netherlands) \n"
          "7. Primeira Liga (Portugal) \n"
          "8. Belgian Pro League (Belgium) \n"
          "9. Scottish Premiership (Scotland) \n"
          "10. Austrian Bundesliga (Austria)")

    league_mapping = {
        '1': settings.ENG,
        '2': settings.ESP,
        '3': settings.GER,
        '4': settings.FRA,
        '5': settings.ITA,
        '6': settings.NED,
        '7': settings.POR,
        '8': settings.BEL,
        '9': settings.SCO,
        '10': settings.AUS
    }

    user_input = input("Enter the league number: ")
    return league_mapping.get(user_input)


def select_teams_from_league(country):
    country_name = country["name"]
    teams = country["teams"]
    europe_places = country["europe"]
    create_teams_table(country_name)  # Create the league table if it doesn't exist
    teams_obj = get_teams(league=country_name)
    # Checks if the database is empty
    if len(teams_obj) == 0:
        # Get original teams from settings
        teams_obj, teams_name = get_default_teams_country(teams, country_name)
    else:
        teams_name = [team.name for team in teams_obj]

    if country_name is None or teams_obj is None or teams_name is None:
        raise ValueError("Invalid value")

    print(f"Country: {country_name}")
    print(f"Teams: {teams_name}")

    return country_name, teams_obj, teams_name, europe_places


def league_simulation(league, teams, europe):
    """
        Simulate a league by playing the fixtures, updating the teams and generating the standings
    :param europe: How many places are for UCL, UEL, UECL
    :param league: The league we want to simulate
    :param teams: The teams found in the league
    :return:
    """
    matches.play_fixture_league(teams)

    for team in teams:
        update_team(team, league)  # Update team data in the database

    return matches.generate_standings(teams, league, europe)


def cup_simulation(league, teams):
    sorted_teams = sorted(teams, key=lambda x: x.skill, reverse=True)
    if len(teams) >= 16:
        new_teams = sorted_teams[:16]
    else:
        new_teams = sorted_teams[:8]

    teams = matches.play_country_cup(new_teams, league)

    for team in teams:
        update_team(team, league)  # Update team data in the database
    return teams


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
