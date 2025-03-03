from pathlib import Path

from database import create_teams_table, get_teams, update_team, update_general_table_european_spots
from src import settings
from team import Team


def select_teams_from_league(country):
    country_name = country["name"]
    teams = country["teams"]
    europe_places = country["europe"]
    first_division_teams = country["first_division_teams"]
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

    return country_name, teams_obj, teams_name, europe_places, first_division_teams


def league_simulation(league, teams, europe, max_teams_in_first_division=12):
    """
        Simulate a league by playing the fixtures, updating the teams, and generating the standings.
        If the number of teams exceeds the max for the first division, split into divisions.
    :param league: The league we want to simulate.
    :param teams: The teams found in the league.
    :param europe: How many places are for UCL, UEL, UECL.
    :param max_teams_in_first_division: Max number of teams allowed in the first division.
    :return: Combined list of all teams objects.
    """
    # Step 1: Sort teams by skill (descending) for accurate division placement
    teams.sort(key=lambda x: x.skill, reverse=True)

    # Step 2: Split teams into divisions
    divisions = {}
    division_number = 1
    original_teams = teams
    while teams:
        divisions[division_number] = teams[:max_teams_in_first_division]
        teams = teams[max_teams_in_first_division:]  # Remove teams added to this division
        division_number += 1

    # Step 3: Simulate leagues for each division and combine all teams objects
    all_teams_objects = []
    for division_number, division_teams in divisions.items():

        play_fixture_league(division_teams)

        if division_number == 1:
            # Generate standings with Europe for the top division only
            print(f"Simulating Division {division_number} with European spots")
            division_team_objects = generate_standings(division_teams, league, europe, division_number)
        else:
            # Generate standings without Europe for lower divisions
            print(f"Simulating Division {division_number}")
            division_team_objects = generate_standings(division_teams, league, None, division_number)

        # Combine teams into a single list
        all_teams_objects.extend(division_team_objects)

    # Step 4: Update teams in the database
    for team in original_teams:
        update_team(team, league)  # Update team data in the database

    return all_teams_objects

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


def generate_fixtures_league(teams):
    fixtures = []
    rounds = len(teams) - 1

    for _ in range(rounds):
        round_fixtures = []
        half_round = len(teams) // 2
        for i in range(half_round):
            fixture = (teams[i], teams[-i - 1])
            round_fixtures.append(fixture)
        fixtures.append(round_fixtures)
        teams.insert(1, teams.pop())

    # Returns double the number of fixtures because of the 2 times schedule in leagues
    return fixtures + fixtures


def play_fixture_league(teams):
    """
        Simulates a league season by playing all fixtures.
        Handles both single round-robin and double round-robin fixtures.
    :param teams: List of teams in the league.
    :return: Teams with updated statistics after simulating all fixtures.
    """
    # Generate fixtures (home and away matches for each pair)
    fixtures = generate_fixtures_league(teams)

    # Play each round of fixtures
    for _, round_fixtures in enumerate(fixtures):
        for home, away in round_fixtures:
            home.play_match(away)

    # Update all teams after the fixtures are played
    for team in teams:
        team.update_current()

    return teams

def generate_standings(teams, league, europe, division):

    # Sort teams based on points, wins, and goals scored (descending order)
    teams.sort(key=lambda x: (x.current['points'], x.current['wins'], x.current['scored']), reverse=True)
    # Prepare the league results file
    league_text = Path(f"{settings.RESULTS_FOLDER}/{league}.txt")
    league_text.touch(exist_ok=True)

    with open(league_text, 'a', encoding="utf-8") as file:
        file.write(f"--- Final Standings ---")

    if division == 1:

        for i, team in enumerate(teams):
            if i == 0:
                with open(league_text, 'a',  encoding="utf-8") as file:
                    file.write(f"Winner of {league} - Division {division}: {team.name}\n")
                print(f"Winner of {league} - Division {division}: {team.name}")
                winners_file = Path(f"{settings.RESULTS_FOLDER}/{settings.WINNERS_TEXT}")
                winners_file.touch(exist_ok=True)
                with open(winners_file, 'a',  encoding="utf-8") as winners:
                    winners.write(f"Winner of {league} - Division {division}: {team.name}\n")
                team.first_place += 1
                update_team(team, league)
            elif i == 1:
                team.second_place += 1
                update_team(team, league)
            elif i == 2:
                team.third_place += 1
                update_team(team, league)

            # Extract the number of European qualification spots from the `europe` parameter
            cl_places_lp = europe["UCL"][0]
            cl_places_q2 = europe["UCL"][1]
            cl_places_q1 = europe["UCL"][2]

            el_places_lp = europe["UEL"][0]
            el_places_q2 = europe["UEL"][1]
            el_places_q1 = europe["UEL"][2]

            ecl_places_lp = europe["UECL"][0]
            ecl_places_q2 = europe["UECL"][1]
            ecl_places_q1 = europe["UECL"][2]

            # Define stages with the corresponding number of places
            europe_stages = [
                (cl_places_lp, f"{settings.UCL} - League Phase"),
                (cl_places_q2, f"{settings.UCL} - Round 2"),
                (cl_places_q1, f"{settings.UCL} - Round 1"),
                (el_places_lp, f"{settings.UEL} - League Phase"),
                (el_places_q2, f"{settings.UEL} - Round 2"),
                (el_places_q1, f"{settings.UEL} - Round 1"),
                (ecl_places_lp, f"{settings.UECL} - League Phase"),
                (ecl_places_q2, f"{settings.UECL} - Round 2"),
                (ecl_places_q1, f"{settings.UECL} - Round 1"),
            ]

            # Use a running total to avoid repetitive sums
            threshold = 0
            for places, stage in europe_stages:
                threshold += places
                if i < threshold:
                    team.europe = stage
                    break
            else:
                team.europe = "No qualification"

            update_general_table_european_spots(team)
            current_team = team.current
            with open(league_text, 'a', encoding="utf-8") as file:
                file.write(
                    f"{i + 1}. {team.name} - {current_team['points']} points - {current_team['wins']} wins - "
                    f"{current_team['draws']} draws - {current_team['losses']} losses"
                    f" - {current_team['scored']} scored - {current_team['against']} against - {team.europe}\n")

    else:
        for i, team in enumerate(teams):
            if i == 0:
                with open(league_text, 'a', encoding="utf-8") as file:
                    file.write(f"Winner of {league} - Division {division}: {team.name}\n")
                print(f"Winner of {league} - Division {division}: {team.name}")
                winners_file = Path(f"{settings.RESULTS_FOLDER}/{settings.WINNERS_TEXT}")
                winners_file.touch(exist_ok=True)
                with open(winners_file, 'a', encoding="utf-8") as winners:
                    winners.write(f"Winner of {league} - Division {division}: {team.name}\n")

            team.europe = "No qualification"

            update_general_table_european_spots(team)
            current_team = team.current
            with open(league_text, 'a', encoding="utf-8") as file:
                file.write(
                    f"{i + 1}. {team.name} - {current_team['points']} points - {current_team['wins']} wins - "
                    f"{current_team['draws']} draws - {current_team['losses']} losses"
                    f" - {current_team['scored']} scored - {current_team['against']} against - {team.europe}\n")

    return teams
