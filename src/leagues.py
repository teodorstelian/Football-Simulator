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
          "10. Austrian Bundesliga (Austria) \n"
          "11. Romanian League (Romania) \n"
          "12. Swiss Super League (Switzerland) \n"
          "13. Turkish Super League (Turkey) \n"
          "14. Greek Super League (Greece) \n"
          "15. Czech First League (Czech Republic) \n"
          "16. Ekstraklasa (Poland) \n"
          "17. Russian Premier League (Russia) \n"
          "18. Ukrainian Premier League (Ukraine) \n"
          "19. Serbian SuperLiga (Serbia)")

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
        '10': settings.AUS,
        '11': settings.ROM,
        '12': settings.SUI,
        '13': settings.TUR,
        '14': settings.GRE,
        '15': settings.CZE,
        '16': settings.POL,
        '17': settings.RUS,
        '18': settings.UKR,
        '19': settings.SRB
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
    if len(teams) >= 32:
        new_teams = sorted_teams[:32]
    elif len(teams) >= 16:
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
