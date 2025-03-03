import math
import random
from pathlib import Path

from src import settings
from src.database import update_team, update_team_parameter


def cup_simulation(league, teams):
    sorted_teams = sorted(teams, key=lambda x: x.skill, reverse=True)
    if len(teams) >= 32:
        new_teams = sorted_teams[:32]
    elif len(teams) >= 16:
        new_teams = sorted_teams[:16]
    elif len(teams) >= 8:
        new_teams = sorted_teams[:8]
    else:
        new_teams = sorted_teams[:4]

    teams = play_country_cup(new_teams, league)

    for team in teams:
        update_team(team, league)  # Update team data in the database
    return teams

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

def get_round_name(number_teams):
    if number_teams == 2:
        return "Final"
    elif number_teams == 4:
        return "Semi-Final"
    elif number_teams == 8:
        return "Quarter-Final"
    else:
        return None
