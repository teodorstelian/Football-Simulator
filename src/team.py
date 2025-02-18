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

    @staticmethod
    def calculate_goals(skill_level, opponent_skill_level, is_home):
        """
        Calculates goals scored based on skills and home advantage.
        """
        base = 1.5  # Base value for average goals
        skill_diff = (skill_level - opponent_skill_level) / 15
        home_advantage = 0.5 if is_home else 0  # Slight boost for home teams
        max_goals = max(0, random.gauss(base + skill_diff + home_advantage, 1))
        return round(max_goals)

    def play_match(self, opponent, knockouts=False, has_2_legs=False, file=None):
        """
        Simulates a match or two-legged tie between self and the opponent.
        :param opponent: The opposing team
        :param knockouts: True if the match requires a winner (e.g., knockout round)
        :param has_2_legs: True if the match is played over two legs (home and away)
        :param file: Output file to log match results
        :return: The winning team object or "Draw" if no winner
        """

        def log_message(message):
            """Logs or prints messages."""
            print(message)
            if file:
                with open(file, 'a') as f:
                    f.write(message + '\n')

        def calculate_aggregate_and_winner(scores_self, scores_opponent):
            """Calculates aggregate scores and determines the winner."""
            self_aggregate = sum(scores_self)
            opponent_aggregate = sum(scores_opponent)
            log_message(f"Aggregate Score: {self.name} {self_aggregate} - {opponent_aggregate} {opponent.name}")
            if self_aggregate > opponent_aggregate:
                log_message(f"{self.name} advances!")
                return self, self_aggregate, opponent_aggregate
            elif self_aggregate < opponent_aggregate:
                log_message(f"{opponent.name} advances!")
                return opponent, self_aggregate, opponent_aggregate
            return None, self_aggregate, opponent_aggregate  # Tie

        def handle_tie_breaking(self_aggregate, opponent_aggregate):
            """Handles tie-breaking logic for knockout matches."""
            log_message("Aggregate is tied! Proceeding to extra time...")
            result = "Draw"
            while result == "Draw":
                extra_self_score = random.randint(0, 1)
                extra_opponent_score = random.randint(0, 1)
                self_aggregate += extra_self_score
                opponent_aggregate += extra_opponent_score
                result = self.match_with_extra_time(extra_self_score, extra_opponent_score, opponent, file)
            return result, self_aggregate, opponent_aggregate

        if has_2_legs:
            scores_self = [
                self.calculate_goals(self.skill, opponent.skill, is_home=True),
                self.calculate_goals(self.skill, opponent.skill, is_home=False)
            ]
            scores_opponent = [
                self.calculate_goals(opponent.skill, self.skill, is_home=False),
                self.calculate_goals(opponent.skill, self.skill, is_home=True)
            ]

            log_message(f"1st Leg: {self.name} (Home) {scores_self[0]} - {scores_opponent[0]} {opponent.name} (Away)")
            log_message(f"2nd Leg: {opponent.name} (Home) {scores_opponent[1]} - {scores_self[1]} {self.name} (Away)")

            winner, self_aggregate, opponent_aggregate = calculate_aggregate_and_winner(scores_self, scores_opponent)

            if not winner and knockouts:  # Handle tie in knockouts
                winner, self_aggregate, opponent_aggregate = handle_tie_breaking(self_aggregate, opponent_aggregate)

            self.update_goals(opponent, self_aggregate, opponent_aggregate)
            return winner or "Draw"

        # Single-leg match
        goals_self = self.calculate_goals(self.skill, opponent.skill, is_home=True)
        goals_opponent = self.calculate_goals(opponent.skill, self.skill, is_home=False)
        log_message(f"{self.name} {goals_self} - {goals_opponent} {opponent.name}")

        if goals_self > goals_opponent:
            self.current["wins"] += 1
            opponent.current["losses"] += 1
            log_message(f"{self.name} won against {opponent.name}")
            winner = self
        elif goals_self < goals_opponent:
            opponent.current["wins"] += 1
            self.current["losses"] += 1
            log_message(f"{opponent.name} won against {self.name}")
            winner = opponent
        else:
            if knockouts:
                winner, goals_self, goals_opponent = handle_tie_breaking(goals_self, goals_opponent)
            else:
                self.current["draws"] += 1
                opponent.current["draws"] += 1
                log_message(f"{self.name} drew with {opponent.name}")
                winner = "Draw"

        self.update_goals(opponent, goals_self, goals_opponent)
        return winner

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
