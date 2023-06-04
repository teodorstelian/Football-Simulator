import random


def generate_fixtures(teams):
    fixtures = [(teams[i], teams[j]) for i in range(len(teams)) for j in range(i + 1, len(teams))]

    for _ in range(1, len(teams)):
        print(f"--- Round {_} ---")
        random.shuffle(fixtures)
        for home_team, away_team in fixtures:
            home_team.play_match(away_team)


def generate_standings(teams):
    print("--- Final Standings ---")
    teams.sort(key=lambda x: (x.points, x.wins, x.goals_scored), reverse=True)
    for i, team in enumerate(teams):
        print(
            f"{i + 1}. {team.name} - {team.points} points - {team.wins} wins - {team.draws} draws - {team.losses} losses"
            f" - {team.goals_scored} scored - {team.goals_against} against")
