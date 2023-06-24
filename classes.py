import random
from math import ceil


class Team:
    def __init__(self, name, country, skill, league_titles=0, ucl=0, uel=0, uecl=0,
                 matches=0, wins=0, draws=0, losses=0, points=0, scored=0, against=0):
        self.name = name
        self.country = country
        self.skill = skill
        self.league_titles = league_titles
        self.ucl = ucl
        self.uel = uel
        self.uecl = uecl
        self.points = points
        self.matches_played = matches
        self.goals_scored = scored
        self.goals_against = against
        self.wins = wins
        self.draws = draws
        self.losses = losses

    def play_match(self, opponent):
        self.matches_played += 1
        opponent.matches_played += 1
        skill_diff = int(self.skill[0]) - int(opponent.skill[0])
        losing_max = ceil(3-(skill_diff/10))
        winning_max = ceil(3+(skill_diff/10))
        goals_scored = random.randint(0, winning_max)
        goals_conceded = random.randint(0, losing_max)
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
