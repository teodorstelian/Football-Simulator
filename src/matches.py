import math
from pathlib import Path

import settings


def play_european_cup(teams, competition):
    competition_text = Path(f"{settings.RESULTS_FOLDER}/{competition}.txt")
    competition_text.touch(exist_ok=True)
    teams_name = [team.name for team in teams]
    print(teams_name)
    with open(competition_text, 'a') as file:
        file.write(f"Teams of current competition: {teams_name}\n")
    generate_fixtures_cup(teams, competition)


def generate_fixtures_cup(teams, competition):
    num_teams = len(teams)
    num_rounds = int(math.log(num_teams, 2))
    current_participants = teams
    competition_text = Path(f"{settings.RESULTS_FOLDER}/{competition}.txt")
    competition_text.touch(exist_ok=True)

    for round_num in range(num_rounds):
        round_name = f"Round {str(round_num + 1)}"
        with open(competition_text, 'a') as file:
            file.write(f"Current round: {round_name}\n")
        print(round_name)
        next_round = []

        for i in range(0, len(current_participants), 2):
            home = current_participants[i]
            away = current_participants[i + 1]
            winner = home.play_match(away, knockouts=True, file=competition_text)
            next_round.append(winner)
        for team in current_participants:
            team.update_current()
        current_participants = next_round

    winner = current_participants[0].name
    if competition == settings.UCL:
        current_participants[0].ucl += 1
    elif competition == settings.UEL:
        current_participants[0].uel += 1
    elif competition == settings.UECL:
        current_participants[0].uecl += 1
    print("Overall Winner:", winner)
    with open(competition_text, 'a') as file:
        file.write(f"Winner of {competition}: {winner}\n")
    winners_file = Path(f"{settings.RESULTS_FOLDER}/{settings.WINNERS_TEXT}")
    winners_file.touch(exist_ok=True)
    with open(winners_file, 'a') as winners:
        winners.write(f"Winner of {competition}: {winner}\n")


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
                file.write(f"Winner of {league}: {team.name}\n")
            print(f"Winner of {league}: {team.name}")
            winners_file = Path(f"{settings.RESULTS_FOLDER}/{settings.WINNERS_TEXT}")
            winners_file.touch(exist_ok=True)
            with open(winners_file, 'a') as winners:
                winners.write(f"Winner of {league}: {team.name}\n")
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
