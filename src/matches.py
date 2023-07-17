import math
from pathlib import Path

import settings


def play_country_cup(teams, country):
    competition_text = Path(f"{settings.RESULTS_FOLDER}/{country}.txt")
    competition_text.touch(exist_ok=True)
    teams_name = [team.name for team in teams]
    print(teams_name)
    teams, winner_obj = generate_fixtures_cup(teams, country)
    winner_name = winner_obj.name
    print("Overall Winner:", winner_name)
    with open(competition_text, 'a') as file:
        file.write(f"Winner of {country} Cup: {winner_name}\n")
    winners_file = Path(f"{settings.RESULTS_FOLDER}/{settings.WINNERS_TEXT}")
    winners_file.touch(exist_ok=True)
    with open(winners_file, 'a') as winners:
        winners.write(f"Winner of {country} Cup: {winner_name}\n")
    for team in teams:
        team.update_current()
    setattr(winner_obj, "cup_titles", getattr(winner_obj, "cup_titles") + 1)
    return teams


def play_european_cup(teams, competition):
    competition_text = Path(f"{settings.RESULTS_FOLDER}/{competition}.txt")
    competition_text.touch(exist_ok=True)
    teams_name = [team.name for team in teams]
    print(teams_name)
    with open(competition_text, 'a') as file:
        file.write(f"Teams of current competition: {teams_name}\n")
    teams, winner_obj = generate_fixtures_cup(teams, competition, logging=True)
    winner_name = winner_obj.name
    print("Overall Winner:", winner_name)
    with open(competition_text, 'a') as file:
        file.write(f"Winner of {competition}: {winner_name}\n")
    winners_file = Path(f"{settings.RESULTS_FOLDER}/{settings.WINNERS_TEXT}")
    winners_file.touch(exist_ok=True)
    with open(winners_file, 'a') as winners:
        winners.write(f"Winner of {competition}: {winner_name}\n")
    for team in teams:
        team.update_current()
    competition_mapping = {
        settings.UCL: "ucl",
        settings.UEL: "uel",
        settings.UECL: "uecl"
    }
    if competition in competition_mapping:
        setattr(winner_obj, competition_mapping[competition], getattr(winner_obj, competition_mapping[competition]) + 1)
    return teams


def generate_fixtures_cup(teams, competition, logging=None):
    num_teams = len(teams)
    num_rounds = int(math.log(num_teams, 2))
    current_participants = teams
    if logging:
        logging = Path(f"{settings.RESULTS_FOLDER}/{competition}.txt")
        logging.touch(exist_ok=True)

    for round_num in range(num_rounds):
        round_name = f"Round {str(round_num + 1)}"
        if logging:
            with open(logging, 'a') as file:
                file.write(f"Current round: {round_name}\n")
        print(round_name)
        next_round = []

        for i in range(0, len(current_participants), 2):
            home = current_participants[i]
            away = current_participants[i + 1]
            winner = home.play_match(away, knockouts=True, file=logging)
            next_round.append(winner)
        current_participants = next_round

    return teams, current_participants[0]


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
        print(f"Round {_ + 1}:")
        for home, away in round_fixtures:
            home.play_match(away)

    for team in teams:
        team.update_current()


def generate_standings(teams, league, europe):
    print("--- Final Standings ---")
    teams.sort(key=lambda x: (x.current['points'], x.current['wins'], x.current['scored']), reverse=True)
    cl_places = europe[0]
    el_places = europe[1]
    ecl_places = europe[2]
    league_text = Path(f"{settings.RESULTS_FOLDER}/{league}.txt")
    league_text.touch(exist_ok=True)

    for i, team in enumerate(teams):
        if i == 0:
            with open(league_text, 'a') as file:
                file.write(f"Winner of League: {team.name}\n")
            print(f"Winner of {league}: {team.name}")
            winners_file = Path(f"{settings.RESULTS_FOLDER}/{settings.WINNERS_TEXT}")
            winners_file.touch(exist_ok=True)
            with open(winners_file, 'a') as winners:
                winners.write(f"Winner of {league} League: {team.name}\n")
            team.league_titles += 1
            team.europe = settings.UCL
        elif i < cl_places:
            team.europe = settings.UCL
        elif i < cl_places + el_places:
            team.europe = settings.UEL
        elif i < cl_places + el_places + ecl_places:
            team.europe = settings.UECL
        else:
            team.europe = "No qualification"
        current_team = team.current
        with open(league_text, 'a') as file:
            file.write(
                f"{i + 1}. {team.name} - {current_team['points']} points - {current_team['wins']} wins - "
                f"{current_team['draws']} draws - {current_team['losses']} losses"
                f" - {current_team['scored']} scored - {current_team['against']} against - {team.europe}\n")
        print(
            f"{i + 1}. {team.name} - {current_team['points']} points - {current_team['wins']} wins - "
            f"{current_team['draws']} draws - {current_team['losses']} losses"
            f" - {current_team['scored']} scored - {current_team['against']} against - {team.europe}")

    return teams
