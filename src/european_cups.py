from pathlib import Path

from src import settings
from src.database import get_team_coefficients, update_european_competition_round_team


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
        "Quarter-Final": {"teams": 8, "db_name": "quarter_finals"},
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