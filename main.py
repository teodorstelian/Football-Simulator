import random


class Team:
    def __init__(self, name):
        self.name = name
        self.points = 0
        self.matches_played = 0
        self.goals_scored = 0
        self.goals_against = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0

    def play_match(self, opponent):
        self.matches_played += 1
        goals_scored = random.randint(0, 5)
        goals_conceded = random.randint(0, 5)
        if goals_scored > goals_conceded:
            self.points += 3
            self.wins += 1
            opponent.losses += 1
            print(f"{self.name} won against {opponent.name} {goals_scored} - {goals_conceded}")
        elif goals_scored < goals_conceded:
            opponent.points += 3
            opponent.wins += 1
            self.losses += 1
            print(f"{opponent.name} won against {self.name} {goals_scored} - {goals_conceded}")
        else:
            self.points += 1
            opponent.points += 1
            self.draws += 1
            opponent.draws += 1
            print(f"{self.name} drew with {opponent.name} {goals_scored} - {goals_conceded}")
        self.goals_scored += goals_scored
        self.goals_against += goals_conceded
        opponent.goals_scored += goals_conceded
        opponent.goals_against += goals_scored


teams = [
    Team("Team A"),
    Team("Team B"),
    Team("Team C"),
    Team("Team D"),
]

fixtures = [(teams[i], teams[j]) for i in range(len(teams)) for j in range(i + 1, len(teams))]

for round in range(1, len(teams)):
    print(f"--- Round {round} ---")
    random.shuffle(fixtures)
    for home_team, away_team in fixtures:
        home_team.play_match(away_team)

print("--- Final Standings ---")
teams.sort(key=lambda x: (x.points, x.wins, x.goals_scored), reverse=True)
for i, team in enumerate(teams):
    print(
        f"{i + 1}. {team.name} - {team.points} points - {team.wins} wins - {team.draws} draws - {team.losses} losses - {team.goals_scored} scored - {team.goals_against} against")
