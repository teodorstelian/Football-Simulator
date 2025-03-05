import random
from collections import defaultdict
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
        "Round 1": {"teams": 64, "db_name": "q1"},
        "Round 2": {"teams": 64, "db_name": "q2"},
        "League Phase": {"teams": 36, "db_name": "league_phase"},
        "Round of 32": {"teams": 16, "db_name": "round_of_32"},
        "Round of 16": {"teams": 16, "db_name": "round_of_16"},
        "Quarter-Final": {"teams": 8, "db_name": "quarter_finals"},
        "Semi-Final": {"teams": 4, "db_name": "semi_finals"},
        "Final": {"teams": 2, "db_name": "finals"}
    }

    # Split teams into Round 1 and Round 2 based on their 'europe' field
    round_1_teams = [team for team in teams if "Round 1" in team.europe]
    round_2_teams = [team for team in teams if "Round 2" in team.europe]
    league_phase_teams = [team for team in teams if "League Phase" in team.europe]

    # Log Round 1 teams
    with open(competition_text, 'a',  encoding="utf-8") as file:
        file.write(f"Teams starting in {competition} Round 1: {[team.name for team in round_1_teams]}\n")

    round_1_winners = generate_single_round(round_1_teams, competition, has_2_legs=True, logging=True, eur_round=stages["Round 1"]["db_name"])

    # Log teams advanced
    with open(competition_text, 'a',  encoding="utf-8") as file:
        file.write(f"Round 1 Winners: {[team.name for team in round_1_winners]}\n")
        file.write(f"Round 2 Qualified: {[team.name for team in round_2_teams]}\n")

    # Combine Round 1 winners with Round 2 teams
    remaining_teams = round_1_winners + round_2_teams

    # Log Round 2 teams
    with open(competition_text, 'a',  encoding="utf-8") as file:
        file.write(f"Teams advancing to Round 2: {[team.name for team in remaining_teams]}\n")

    round_2_winners = generate_single_round(remaining_teams, competition, has_2_legs=True, logging=True,
                                            eur_round=stages["Round 2"]["db_name"])

    # Log teams advanced
    with open(competition_text, 'a',  encoding="utf-8") as file:
        file.write(f"Round 2 Winners: {[team.name for team in round_2_winners]}\n")
        file.write(f"League Phase Qualified: {[team.name for team in league_phase_teams]}\n")

    # Combine Round 2 winners with League Phase teams
    remaining_teams = round_2_winners + league_phase_teams

    # Log League Phase Teams
    with open(competition_text, 'a', encoding="utf-8") as file:
        file.write(f"Teams advancing to League Phase: {[team.name for team in remaining_teams]}\n")

    # Play League Phase
    league_results = play_league_phase(remaining_teams, competition, logging=True)
    top_8 = league_results["top_8"]
    playoff_teams = league_results["playoffs"]
    eliminated_teams = league_results["eliminated"]

    # Log results of the League Phase
    with open(competition_text, 'a', encoding="utf-8") as file:
        file.write(f"Top 8 advancing to Round of 16: {[team.name for team in top_8]}\n")
        file.write(f"Teams advancing to Knockout Play-offs: {[team.name for team in playoff_teams]}\n")
        file.write(f"Eliminated Teams: {[team.name for team in eliminated_teams]}\n")

    # Play Knockout Play-off Round for teams ranked 9th to 24th
    playoff_winners = generate_single_round(playoff_teams, competition, has_2_legs=True, logging=True,
                                            eur_round=stages["Round of 32"]["db_name"])

    # Combine top 8 with play-off winners for Round of 16
    remaining_teams = top_8 + playoff_winners

    # Play the knockout stages from Round of 16 onwards
    for stage_name, stage_info in stages.items():
        if stage_name in ["Round 1", "Round 2", "League Phase", "Round of 32"]:
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

def play_league_phase(teams, competition, logging=False):
    """
    Simulates the League Phase between Round 2 and Round of 32.

    :param teams: List of 36 teams participating in the league phase.
    :param competition: Name of the competition.
    :param logging: Boolean to log match and ranking information.
    :return: A dictionary containing the final rankings and team statuses.
    """

    if len(teams) != 36:
        raise ValueError("League Phase requires exactly 36 teams!")

    # Prepare competition log file if logging is enabled
    competition_text = Path(f"{settings.RESULTS_FOLDER}/{competition}.txt")
    if logging:
        competition_text.touch(exist_ok=True)

    # Fetch coefficients for all teams
    team_coefficients = get_team_coefficients(teams, competition)

    # Sort teams by coefficients (descending)
    teams.sort(key=lambda team: team_coefficients.get(team.name, 0), reverse=True)

    # Divide teams into 4 pools (Pot 1: best coefficients, Pot 4: lowest coefficients)
    pools = {
        "Pot 1": teams[:9],
        "Pot 2": teams[9:18],
        "Pot 3": teams[18:27],
        "Pot 4": teams[27:]
    }

    if logging:
        with open(competition_text, 'a', encoding="utf-8") as log_file:
            log_file.write(f"--- League Phase Pools for {competition} ---\n")
            for pot_name, pot in pools.items():
                log_file.write(f"{pot_name}: {[team.name for team in pot]}\n")
            log_file.write("---------------------------------------------------\n")

    for team in teams:
        update_european_competition_round_team(team.name, competition, "league_phase")

    # Initialize league table
    league_table = {team.name: {"points": 0, "goals_scored": 0, "goals_conceded": 0} for team in teams}

    # Generate matches ensuring fairness
    matchups = defaultdict(list)  # Tracks matches for each team

    # Generate matches: Each team plays eight matches (2 against each pot: 1 home, 1 away)
    for team in teams:
        opponents = []

        # Select 2 opponents from each pot (excluding the team's current pot)
        for pot_name, pot in pools.items():
            if team in pot:
                continue
            pot_opponents = [opponent for opponent in pot if
                             opponent not in opponents and team not in matchups[opponent]]
            selected = random.sample(pot_opponents, k=2)  # Randomly pick 2 opponents
            opponents.extend(selected)

        # Shuffle to distribute home and away matches fairly
        random.shuffle(opponents)
        home_matches = opponents[:4]
        away_matches = opponents[4:]

        for home_opponent in home_matches:
            home, away, scored, conceded = team.play_match(home_opponent, knockouts=False, has_2_legs=False,
                                                           file=competition_text if logging else None,
                                                           return_all_info=True)
            update_league_table(league_table, home, away, scored, conceded)
            matchups[team].append(home_opponent)

        for away_opponent in away_matches:
            away, home, conceded, scored = away_opponent.play_match(team, knockouts=False, has_2_legs=False,
                                                                    file=competition_text if logging else None,
                                                                    return_all_info=True)
            update_league_table(league_table, home, away, scored, conceded)
            matchups[team].append(away_opponent)

    # Sort league table by points (then by goal difference, then by goals scored)
    ranked_teams = sorted(teams, key=lambda t: (
        league_table[t.name]["points"],
        league_table[t.name]["goals_scored"] - league_table[t.name]["goals_conceded"],
        league_table[t.name]["goals_scored"]
    ), reverse=True)

    if logging:
        with open(competition_text, 'a', encoding="utf-8") as log_file:
            log_file.write(f"--- Final League Table for {competition} ---\n")
            for idx, team in enumerate(ranked_teams, start=1):
                stats = league_table[team.name]
                log_file.write(f"{idx}. {team.name} - Points: {stats['points']}, "
                               f"Goal Difference: {stats['goals_scored'] - stats['goals_conceded']}, "
                               f"Goals Scored: {stats['goals_scored']}\n")

    # Determine outcomes
    top_8 = ranked_teams[:8]  # Advance directly to Round of 16
    playoff_teams = ranked_teams[8:24]  # Qualify for knockout phase play-offs
    eliminated_teams = ranked_teams[24:]  # Out of all competitions

    return {"top_8": top_8, "playoffs": playoff_teams, "eliminated": eliminated_teams}


def update_league_table(league_table, home_team, away_team, home_goals, away_goals):
    """
    Updates the league table after a match.
    """
    if home_goals > away_goals:
        league_table[home_team]["points"] += 3
    elif home_goals < away_goals:
        league_table[away_team]["points"] += 3
    else:
        league_table[home_team]["points"] += 1
        league_table[away_team]["points"] += 1

    league_table[home_team]["goals_scored"] += home_goals
    league_table[home_team]["goals_conceded"] += away_goals
    league_table[away_team]["goals_scored"] += away_goals
    league_table[away_team]["goals_conceded"] += home_goals
