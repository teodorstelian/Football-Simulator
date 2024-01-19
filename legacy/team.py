import random
from math import ceil


class Team:
    def __init__(self, name, country, skill, league_titles=0, cup_titles=0, ucl=0, uel=0, uecl=0, europe="No Europe",
                 matches=0, wins=0, draws=0, losses=0, points=0, scored=0, against=0):
        self.name = name
        self.country = country
        self.skill = skill
        self.league_titles = league_titles
        self.cup_titles = cup_titles
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
        self.current = {"points": 0,
                        "wins": 0,
                        "draws": 0,
                        "losses": 0,
                        "matches": 0,
                        "scored": 0,
                        "against": 0}

    def update_goals(self, opponent, scored, conceded):
        self.current["scored"] += scored
        self.current["against"] += conceded
        opponent.current["scored"] += conceded
        opponent.current["against"] += scored

    def match_with_extra_time(self, scored, conceded, opponent, file=None):
        if scored > conceded:
            self.current["wins"] += 1
            opponent.current["losses"] += 1
            print(f"{self.name} won against {opponent.name} {scored} - {conceded}")
            if file:
                with open(file, 'a') as file:
                    file.write(f"{self.name} won against {opponent.name} {scored} - {conceded}\n")
            return self
        elif scored < conceded:
            self.current["losses"] += 1
            opponent.current["wins"] += 1
            print(f"{opponent.name} won against {self.name} {conceded} - {scored}")
            if file:
                with open(file, 'a') as file:
                    file.write(f"{opponent.name} won against {self.name} {conceded} - {scored}\n")
            return opponent
        else:
            return "Draw"

    def play_match(self, opponent, knockouts=False, file=None):
        skill_diff = int(self.skill) - int(opponent.skill)
        losing_max = ceil(3 - (skill_diff / 20))
        winning_max = ceil(3 + (skill_diff / 20))
        goals_scored = random.randint(0, winning_max)
        goals_conceded = random.randint(0, losing_max)
        if knockouts:
            result = self.match_with_extra_time(goals_scored, goals_conceded, opponent, file)
            while result == "Draw":
                goals_scored += random.randint(0, winning_max)
                goals_conceded += random.randint(0, losing_max)
                result = self.match_with_extra_time(goals_scored, goals_conceded, opponent, file)
            self.update_goals(opponent, goals_scored, goals_conceded)
            return result
        elif goals_scored > goals_conceded:
            self.current["wins"] += 1
            opponent.current["losses"] += 1
            print(f"{self.name} won against {opponent.name} {goals_scored} - {goals_conceded}")
            if file:
                with open(file, 'a') as file:
                    file.write(f"{self.name} won against {opponent.name} {goals_scored} - {goals_conceded}\n")

        elif goals_scored < goals_conceded:
            opponent.current["wins"] += 1
            self.current["losses"] += 1
            print(f"{opponent.name} won against {self.name} {goals_conceded} - {goals_scored}")
            if file:
                with open(file, 'a') as file:
                    file.write(f"{opponent.name} won against {self.name} {goals_conceded} - {goals_scored}\n")
        else:
            self.current["draws"] += 1
            opponent.current["draws"] += 1
            print(f"{self.name} drew with {opponent.name} {goals_scored} - {goals_conceded}")
            if file:
                with open(file, 'a') as file:
                    file.write(f"{self.name} drew with {opponent.name} {goals_scored} - {goals_conceded}\n")
        self.update_goals(opponent, goals_scored, goals_conceded)

    def update_current(self):
        self.wins += self.current["wins"]
        self.draws += self.current["draws"]
        self.losses += self.current["losses"]
        self.current["matches"] = self.current["wins"] + self.current["draws"] + self.current["losses"]
        self.matches_played += self.current["matches"]
        self.current["points"] = 3 * self.current["wins"] + self.current["draws"]
        self.points += self.current["points"]
        self.goals_scored += self.current["scored"]
        self.goals_against += self.current["against"]
