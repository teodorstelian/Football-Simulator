import random
from math import ceil


class Team:
    def __init__(self, name, country, skill, league_titles=0, ucl=0, uel=0, uecl=0, europe="No Europe",
                 matches=0, wins=0, draws=0, losses=0, points=0, scored=0, against=0):
        self.name = name
        self.country = country
        self.skill = skill
        self.league_titles = league_titles
        self.ucl = ucl
        self.uel = uel
        self.uecl = uecl
        self.europe = europe
        self.points = points
        self.matches_played = matches
        self.goals_scored = scored
        self.goals_against = against
        self.wins = wins
        self.draws = draws
        self.losses = losses

    def update_goals(self, opponent, scored, conceded):
        self.goals_scored += scored
        self.goals_against += conceded
        opponent.goals_scored += conceded
        opponent.goals_against += scored

    def match_with_extra_time(self, scored, conceded, opponent):
        if scored > conceded:
            self.wins += 1
            opponent.losses += 1
            print(f"{self.name} won against {opponent.name} {scored} - {conceded}")
            return self
        elif scored < conceded:
            opponent.wins += 1
            self.losses += 1
            print(f"{opponent.name} won against {self.name} {scored} - {conceded}")
            return opponent
        else:
            return "Draw"

    def play_match(self, opponent, knockouts = False):
        self.matches_played += 1
        opponent.matches_played += 1
        skill_diff = int(self.skill) - int(opponent.skill)
        losing_max = ceil(3-(skill_diff/20))
        winning_max = ceil(3+(skill_diff/20))
        goals_scored = random.randint(0, winning_max)
        goals_conceded = random.randint(0, losing_max)
        if knockouts:
            result = self.match_with_extra_time(goals_scored, goals_conceded, opponent)
            while result == "Draw":
                goals_scored += random.randint(0, winning_max)
                goals_conceded += random.randint(0, losing_max)
                result = self.match_with_extra_time(goals_scored, goals_conceded, opponent)
            self.update_goals(opponent, goals_scored, goals_conceded)
            return result
        elif goals_scored > goals_conceded:
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
        self.update_goals(opponent, goals_scored, goals_conceded)
