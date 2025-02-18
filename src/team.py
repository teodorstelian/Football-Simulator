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

    def play_match(self, opponent, knockouts=False, has_2_legs=False, file=None):
        """
        Simulates a match or two-legged tie between self and the opponent.
        :param opponent: The opposing team
        :param knockouts: True if the match requires a winner (e.g., knockout round)
        :param has_2_legs: True if the match is played over two legs (home and away)
        :param file: Output file to log match results
        :return: The winning team object or "Draw" if no winner
        """
        # Two-legged logic
        if has_2_legs:
            # First Leg: self (home), opponent (away)
            skill_diff = int(self.skill) - int(opponent.skill)
            home_max_self = ceil(3 + (skill_diff / 20))
            away_max_opponent = ceil(3 - (skill_diff / 20))

            self_home_score = random.randint(0, home_max_self)
            opponent_away_score = random.randint(0, away_max_opponent)
            print(f"1st Leg: {self.name} (Home) {self_home_score} - {opponent_away_score} {opponent.name} (Away)")
            if file:
                with open(file, 'a') as f:
                    f.write(
                        f"1st Leg: {self.name} (Home) {self_home_score} - {opponent_away_score} {opponent.name} (Away)\n")

            # Second Leg: opponent (home), self (away)
            home_max_opponent = ceil(3 + (skill_diff / 20))
            away_max_self = ceil(3 - (skill_diff / 20))

            opponent_home_score = random.randint(0, home_max_opponent)
            self_away_score = random.randint(0, away_max_self)
            print(f"2nd Leg: {opponent.name} (Home) {opponent_home_score} - {self_away_score} {self.name} (Away)")
            if file:
                with open(file, 'a') as f:
                    f.write(
                        f"2nd Leg: {opponent.name} (Home) {opponent_home_score} - {self_away_score} {self.name} (Away)\n")

            # Aggregate scores
            self_aggregate = self_home_score + self_away_score
            opponent_aggregate = opponent_home_score + opponent_away_score
            print(f"Aggregate Score: {self.name} {self_aggregate} - {opponent_aggregate} {opponent.name}")
            if file:
                with open(file, 'a') as f:
                    f.write(f"Aggregate Score: {self.name} {self_aggregate} - {opponent_aggregate} {opponent.name}\n")

            # Determine winner (aggregate)
            if self_aggregate > opponent_aggregate:
                print(f"{self.name} advances!")
                if file:
                    with open(file, 'a') as f:
                        f.write(f"{self.name} advances!\n")
                self.update_goals(opponent, self_aggregate, opponent_aggregate)
                return self
            elif self_aggregate < opponent_aggregate:
                print(f"{opponent.name} advances!")
                if file:
                    with open(file, 'a') as f:
                        f.write(f"{opponent.name} advances!\n")
                self.update_goals(opponent, self_aggregate, opponent_aggregate)
                return opponent
            else:
                # Tie-breaking logic (extra time or penalties)
                if knockouts:
                    print("Aggregate is tied! Proceeding to extra time...")
                    result = self.match_with_extra_time(self_aggregate, opponent_aggregate, opponent, file)
                    while result == "Draw":
                        extra_self_score = random.randint(0, 1)
                        extra_opponent_score = random.randint(0, 1)
                        self_aggregate += extra_self_score
                        opponent_aggregate += extra_opponent_score
                        result = self.match_with_extra_time(extra_self_score, extra_opponent_score, opponent, file)
                    self.update_goals(opponent, self_aggregate, opponent_aggregate)
                    return result
                else:
                    print("Match ends in a draw (no tie-breaking).")
                    return "Draw"

        # Single-leg match logic (regular match)
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
