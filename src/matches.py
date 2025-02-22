import math
import random
from pathlib import Path

import settings
from src.database import update_european_competition_round_team, update_team, \
    update_team_parameter, update_general_table_european_spots, get_team_coefficients


def play_country_cup(teams, country):
    """
    Simulates a domestic country cup and declares a winner.

    :param teams: List of participating teams
    :param country: Name of the country (used for logging the results)
    :return: Updated list of teams
    """
    # Prepare competition result file
    competition_text = Path(f"{settings.RESULTS_FOLDER}/{country}.txt")
    competition_text.touch(exist_ok=True)
    teams_name = [team.name for team in teams]

    with open(competition_text, 'a', encoding="utf-8") as file:
        file.write(f"Teams of {country} Cup: {teams_name}\n")

    # Generate fixtures and determine the winner (single-legged matches for country cups)
    winner_obj = generate_fixtures_cup(teams, country, has_2_legs=False, logging=True)
    winner_name = winner_obj.name
    print(f"Winner of {country} Cup:", winner_name)

    # Log the winner
    with open(competition_text, 'a', encoding="utf-8") as file:
        file.write(f"\nWinner of {country} Cup: {winner_name}\n")
    winners_file = Path(f"{settings.RESULTS_FOLDER}/{settings.WINNERS_TEXT}")
    winners_file.touch(exist_ok=True)
    with open(winners_file, 'a',  encoding="utf-8") as winners:
        winners.write(f"Winner of {country} Cup: {winner_name}\n")

    # Update stats for all teams
    for team in teams:
        team.update_current()

    return teams


def play_european_cup(teams, competition):
    """
    Simulates the European Cup competition (including staggered entry points: Round 1 and Round 2).

    :param teams: List of participating teams (both Round 1 and Round 2 participants)
    :param competition: Name of the competition (e.g., "UCL", "UEL", "UECL")
    :return: Updated list of all teams
    """
    # Prepare competition log file
    competition_text = Path(f"{settings.RESULTS_FOLDER}/{competition}.txt")
    competition_text.touch(exist_ok=True)

    # Define the stages with the required number of teams
    stages = {
        "Round 1": {"teams": 64, "db_name": "Round_1"},
        "Round 2": {"teams": 64, "db_name": "Round_2"},
        "Round of 32": {"teams": 32, "db_name": "round_of_32"},
        "Round of 16": {"teams": 16, "db_name": "round_of_16"},
        "Quarter-Final": {"teams": 8, "db_name": "quarterfinals"},
        "Semi-Final": {"teams": 4, "db_name": "semi_finals"},
        "Final": {"teams": 2, "db_name": "finals"}
    }

    # Split teams into Round 1 and Round 2 based on their 'europe' field
    round_1_teams = [team for team in teams if "Round 1" in team.europe]
    round_2_teams = [team for team in teams if "Round 2" in team.europe]

    # Log Round 1 teams
    with open(competition_text, 'a',  encoding="utf-8") as file:
        file.write(f"Teams starting in {competition} Round 1: {[team.name for team in round_1_teams]}\n")

    # If there are Round 1 teams, play a single round of knockout from Round 1
    if round_1_teams:
        round_1_winners = generate_single_round(round_1_teams, competition, has_2_legs=True, logging=True, eur_round=stages["Round 1"]["db_name"])
    else:
        round_1_winners = []

        # Log Round 2 teams
    with open(competition_text, 'a',  encoding="utf-8") as file:
        file.write(f"Round 1 Winners: {[team.name for team in round_1_winners]}\n")
        file.write(f"Round 2 Qualified: {[team.name for team in round_2_teams]}\n")

    # Combine Round 1 winners with Round 2 teams
    remaining_teams = round_1_winners + round_2_teams

    # Log Round 2 teams
    with open(competition_text, 'a',  encoding="utf-8") as file:
        file.write(f"Teams advancing to Round 2: {[team.name for team in remaining_teams]}\n")

    for stage_name, stage_info in stages.items():
        if stage_name in ["Round 1"]:
            continue

        current_teams = stage_info["teams"]
        if len(remaining_teams) != current_teams:
            raise ValueError(
                f"Invalid team count for '{stage_name}'. Expected {current_teams}, but got {len(remaining_teams)}.")

        if stage_name == "Final":
            final_winner = generate_single_round(remaining_teams, competition, has_2_legs=False, logging=True, eur_round=stages[stage_name]["db_name"])[0]
        else:
            remaining_teams = generate_single_round(remaining_teams, competition, has_2_legs=True, logging=True,  eur_round=stages[stage_name]["db_name"])

    # Log the overall winner
    winner_name = final_winner.name
    print(f"Winner of {competition}:", winner_name)
    with open(competition_text, 'a',  encoding="utf-8") as file:
        file.write(f"\nWinner of {competition}: {winner_name}\n")
    winners_file = Path(f"{settings.RESULTS_FOLDER}/{settings.WINNERS_TEXT}")
    winners_file.touch(exist_ok=True)
    with open(winners_file, 'a',  encoding="utf-8") as winners:
        winners.write(f"Winner of {competition}: {winner_name}\n")
    update_european_competition_round_team(winner_name, competition, "winner")


    # Update stats for all teams
    for team in teams:
        team.update_current()

    return teams

def generate_single_round(teams, competition, has_2_legs=False, logging=False, eur_round=None):
    """
    Plays a single knockout round and returns the winners, ensuring no duplicate matches.

    :param teams: List of teams participating in this round.
    :param competition: Name of the competition.
    :param has_2_legs: Boolean indicating whether matches are two-legged.
    :param logging: Boolean to log match information.
    :return: List of winners.
    """
    if len(teams) % 2 != 0:
        raise ValueError("Teams participating in a knockout round must be even!")

    # Prepare competition log file if logging is enabled
    competition_text = Path(f"{settings.RESULTS_FOLDER}/{competition}.txt")
    if logging:
        competition_text.touch(exist_ok=True)

    next_round = []

    # Fetch coefficients for all teams
    team_coefficients = get_team_coefficients(teams, competition)

    # Sort teams by coefficients (descending) and by skill (descending)
    teams.sort(key=lambda team: (team_coefficients[team.name], team.skill), reverse=True)

    # Write the sorted teams and their coefficients to the log file
    if logging:
        with open(competition_text, 'a', encoding="utf-8") as log_file:
            log_file.write(f"--- Teams Sorted by Coefficients and Skill for {competition} ---\n")
            for idx, team in enumerate(teams, start=1):
                coef = team_coefficients.get(team.name, 0)
                log_file.write(f"{idx}. {team.name} (Coefficient: {coef}, Skill: {team.skill})\n")
            log_file.write("---------------------------------------------------\n")

    while teams:  # Continue until all teams are paired
        home = teams.pop(0)  # Best remaining team
        away = teams.pop(-1)  # Worst remaining team

        # Play the match
        winner = home.play_match(away, knockouts=True, has_2_legs=has_2_legs,
                                 file=competition_text if logging else None)
        if eur_round:
            update_european_competition_round_team(home.name, competition, eur_round)
            update_european_competition_round_team(away.name, competition, eur_round)

        next_round.append(winner)

        # Log the final match result
        if logging:
            with open(competition_text, 'a',  encoding="utf-8") as log_file:
                log_file.write(f"{home.name} vs {away.name}, Winner: {winner.name}\n")

    return next_round

def get_round_name(number_teams):
    if number_teams == 2:
        return "Final"
    elif number_teams == 4:
        return "Semi-Final"
    elif number_teams == 8:
        return "Quarter-Final"
    else:
        return None

def generate_fixtures_cup(teams, competition, has_2_legs=False, prev_rounds=0, logging=False):
    """
    Simulates a knockout-style competition and returns the winner.


    :param teams: A list of teams participating in the cup
    :param competition: Name of the competition
    :param has_2_legs: Boolean indicating whether matches are two-legged
    :param logging: Variable indicating if we need output generated
    :return: The winner of the competition
    """
    # Calculate the number of rounds based on the number of teams (must be power of 2)
    num_rounds = int(math.log(len(teams), 2))
    current_participants = teams

    # Prepare the file for logging, if provided
    competition_text = Path(f"{settings.RESULTS_FOLDER}/{competition}.txt")
    if logging:
        competition_text.touch(exist_ok=True)

    # Iterate through rounds
    for round_num in range(num_rounds):
        # Shuffle the participants before each round
        random.shuffle(current_participants)

        round_name = get_round_name(len(current_participants)) or f"Round {round_num + prev_rounds + 1}"

        if logging:
            with open(competition_text, 'a',  encoding="utf-8") as log_file:
                log_file.write(f"\nCurrent round: {round_name}\n")

        next_round = []

        # Process each match in the current round
        for i in range(0, len(current_participants), 2):
            home = current_participants[i]
            away = current_participants[i + 1]

            if len(current_participants) == 2:
                winner = home.play_match(away, knockouts=True, has_2_legs=False,
                                         file=competition_text if logging else None)
                home.cup_finals += 1
                update_team_parameter(home, competition, "cup_finals", home.cup_finals)
                away.cup_finals += 1
                update_team_parameter(away, competition, "cup_finals", away.cup_finals)
                winner.cup_wins += 1
                update_team_parameter(winner, competition, "cup_wins", home.cup_wins)

            else:
                # Play match (either one-leg or two-leg based on `has_2_legs`)
                winner = home.play_match(away, knockouts=True, has_2_legs=has_2_legs,
                                         file=competition_text if logging else None)
            next_round.append(winner)  # Winners advance to the next round

        # Progress to the next round
        current_participants = next_round

    # Return the sole remaining participant as the winner
    return current_participants[0]


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
    fixtures = generate_fixtures_league(teams)

    for _, round_fixtures in enumerate(fixtures):
        for home, away in round_fixtures:
            home.play_match(away)

    for team in teams:
        team.update_current()


def generate_standings(teams, league, europe):

    # Sort teams based on points, wins, and goals scored (descending order)
    teams.sort(key=lambda x: (x.current['points'], x.current['wins'], x.current['scored']), reverse=True)

    # Extract the number of European qualification spots from the `europe` parameter
    cl_places_r1 = europe["UCL"][0]
    cl_places_r2 = europe["UCL"][1]
    el_places_r1 = europe["UEL"][0]
    el_places_r2 = europe["UEL"][1]
    ecl_places_r1 = europe["UECL"][0]
    ecl_places_r2 = europe["UECL"][1]

    # Prepare the league results file
    league_text = Path(f"{settings.RESULTS_FOLDER}/{league}.txt")
    league_text.touch(exist_ok=True)

    with open(league_text, 'a', encoding="utf-8") as file:
        file.write(f"--- Final Standings ---")

    for i, team in enumerate(teams):
        if i == 0:
            with open(league_text, 'a',  encoding="utf-8") as file:
                file.write(f"Winner of League: {team.name}\n")
            print(f"Winner of {league}: {team.name}")
            winners_file = Path(f"{settings.RESULTS_FOLDER}/{settings.WINNERS_TEXT}")
            winners_file.touch(exist_ok=True)
            with open(winners_file, 'a',  encoding="utf-8") as winners:
                winners.write(f"Winner of {league} League: {team.name}\n")
            team.first_place += 1
            update_team(team, league)
        elif i == 1:
            team.second_place += 1
            update_team(team, league)
        elif i == 2:
            team.third_place += 1
            update_team(team, league)

        # Assign European Competition Qualifications
        if i < cl_places_r1:
            team.europe = f"{settings.UCL} - Round 2"
        elif i < cl_places_r1 + cl_places_r2:
            team.europe = f"{settings.UCL} - Round 1"
        elif i < cl_places_r1 + cl_places_r2 + el_places_r1:
            team.europe = f"{settings.UEL} - Round 2"
        elif i < cl_places_r1 + cl_places_r2 + el_places_r1 + el_places_r2:
            team.europe = f"{settings.UEL} - Round 1"
        elif i < cl_places_r1 + cl_places_r2 + el_places_r1 + el_places_r2 + ecl_places_r1:
            team.europe = f"{settings.UECL} - Round 2"
        elif i <  cl_places_r1 + cl_places_r2 + el_places_r1 + el_places_r2 + ecl_places_r1 + ecl_places_r2:
            team.europe = f"{settings.UECL} - Round 1"
        else:
            team.europe = "No qualification"
        update_general_table_european_spots(team)
        current_team = team.current
        with open(league_text, 'a', encoding="utf-8") as file:
            file.write(
                f"{i + 1}. {team.name} - {current_team['points']} points - {current_team['wins']} wins - "
                f"{current_team['draws']} draws - {current_team['losses']} losses"
                f" - {current_team['scored']} scored - {current_team['against']} against - {team.europe}\n")

    return teams
