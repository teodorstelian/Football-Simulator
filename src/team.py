import random

from src import settings


class Team:
    def __init__(self, name, country, skill, europe="No Europe",
                 matches=0, wins=0, draws=0, losses=0, points=0, scored=0, against=0,
                 first_place=0, second_place=0, third_place=0, cup_finals=0, cup_wins=0):
        self.name = name
        self.country = country
        self.skill = skill
        self.europe = europe
        self.points = points
        self.matches_played = matches
        self.goals_scored = scored
        self.goals_against = against
        self.wins = wins
        self.draws = draws
        self.losses = losses

        self.first_place = first_place
        self.second_place = second_place
        self.third_place = third_place
        self.cup_finals = cup_finals
        self.cup_wins = cup_wins

        self.current = {
            "points": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "matches": 0,
            "scored": 0,
            "against": 0
        }

    def update_goals(self, opponent, scored, conceded):
        """Updates the goals scored and conceded for both teams."""
        self.current["scored"] += scored
        self.current["against"] += conceded
        opponent.current["scored"] += conceded
        opponent.current["against"] += scored

    def determine_match_outcome(self, scored, conceded, opponent, is_aggregate=False):
        """Determines the outcome of the match or aggregate tie."""
        if scored > conceded:
            self.current["wins"] += 1
            opponent.current["losses"] += 1
            return self
        elif scored < conceded:
            opponent.current["wins"] += 1
            self.current["losses"] += 1
            return opponent
        else:
            return "Draw"

    @staticmethod
    def calculate_goals(skill_level, opponent_skill_level, is_home,
                        base_goals=settings.AVG_BASE_GOALS,
                        home_weight=settings.HOME_WEIGHT,
                        skill_weight=settings.SKILL_WEIGHT):
        """
        Calculates goals scored based on skill levels, home advantage, and other parameters.
        """
        skill_diff = (skill_level - opponent_skill_level) / skill_weight
        home_advantage = home_weight if is_home else 0
        max_goals = max(0, random.gauss(base_goals + skill_diff + home_advantage, 1))
        return round(max_goals)

    def play_match(self, opponent, knockouts=False, has_2_legs=False, file=None, return_all_info=None):
        """
        Simulates a match or a two-legged tie.
        :param opponent: The opposing team.
        :param knockouts: True if the match requires a winner (e.g., knockout round).
        :param has_2_legs: True if the match is played over two legs (home and away).
        :param file: Output file to log match results.
        :return: Winning team object or "Draw" if there's no winner.
        """
        log_messages = []

        def log_message(message):
            """Logs or stores messages."""
            log_messages.append(message)

        def handle_tie_breaking(self_aggregate, opponent_aggregate):
            """Handles tie-breaking logic with a single extra time period followed by penalties."""
            log_message("Aggregate is tied! Proceeding to extra time...")

            # Extra time
            extra_self_score = random.randint(0, 1)  # Random score for extra time
            extra_opponent_score = random.randint(0, 1)
            self_aggregate += extra_self_score
            opponent_aggregate += extra_opponent_score
            log_message(
                f"Extra Time: {self.name} {extra_self_score} - {extra_opponent_score} {opponent.name} (Aggregate: {self_aggregate} - {opponent_aggregate})"
            )

            # Determine winner in extra time
            if extra_self_score > extra_opponent_score:
                return self, self_aggregate, opponent_aggregate
            elif extra_self_score < extra_opponent_score:
                return opponent, self_aggregate, opponent_aggregate

            # Penalty shootout if still tied
            log_message("Extra time ends in a draw. Proceeding to penalties!")
            penalties_self = 0
            penalties_opponent = 0

            # Simulate penalties (5 attempts each)
            for i in range(5):  # Standard penalty shootout with 5 penalties each
                if random.random() < 0.7:  # 70% chance of scoring
                    penalties_self += 1
                if random.random() < 0.7:
                    penalties_opponent += 1

            # Log penalty results
            log_message(f"Penalties: {self.name} {penalties_self} - {penalties_opponent} {opponent.name}")

            # Determine winner after penalties
            if penalties_self > penalties_opponent:
                log_message(f"{self.name} wins on penalties!")
                return self, self_aggregate, opponent_aggregate
            elif penalties_self < penalties_opponent:
                log_message(f"{opponent.name} wins on penalties!")
                return opponent, self_aggregate, opponent_aggregate
            else:
                # Sudden death penalties if still tied after 5
                log_message("Penalties are tied! Sudden death begins!")
                while True:
                    if random.random() < 0.7:  # Sudden death penalty for self
                        penalties_self += 1
                    if random.random() < 0.7:  # Sudden death penalty for opponent
                        penalties_opponent += 1

                    # Check if there's a winner
                    if penalties_self != penalties_opponent:
                        log_message(
                            f"Sudden Death: {self.name} {penalties_self} - {penalties_opponent} {opponent.name}")
                        if penalties_self > penalties_opponent:
                            log_message(f"{self.name} wins on sudden death penalties!")
                            return self, self_aggregate, opponent_aggregate
                        else:
                            log_message(f"{opponent.name} wins on sudden death penalties!")
                            return opponent, self_aggregate, opponent_aggregate

        if has_2_legs:
            # Simulate both legs
            scores_self = [
                self.calculate_goals(self.skill, opponent.skill, is_home=True),
                self.calculate_goals(self.skill, opponent.skill, is_home=False)
            ]
            scores_opponent = [
                self.calculate_goals(opponent.skill, self.skill, is_home=False),
                self.calculate_goals(opponent.skill, self.skill, is_home=True)
            ]

            # Log results for both legs
            log_message(f"1st Leg: {self.name} (Home) {scores_self[0]} - {scores_opponent[0]} {opponent.name} (Away)")
            log_message(f"2nd Leg: {opponent.name} (Home) {scores_opponent[1]} - {scores_self[1]} {self.name} (Away)")

            # Calculate aggregate scores and determine winner
            self_aggregate, opponent_aggregate = sum(scores_self), sum(scores_opponent)
            winner = self.determine_match_outcome(self_aggregate, opponent_aggregate, opponent, is_aggregate=True)

            if winner == "Draw" and knockouts:  # Handle tie in knockouts
                winner, self_aggregate, opponent_aggregate = handle_tie_breaking(self_aggregate, opponent_aggregate)

            self.update_goals(opponent, self_aggregate, opponent_aggregate)

            # Save log messages to file if specified
            if file:
                with open(file, 'a',  encoding="utf-8") as f:
                    f.write('\n'.join(log_messages) + '\n')

            return winner or "Draw"

        # Single-leg match
        scored = self.calculate_goals(self.skill, opponent.skill, is_home=True)
        conceded = self.calculate_goals(opponent.skill, self.skill, is_home=False)
        log_message(f"{self.name} {scored} - {conceded} {opponent.name}")

        if scored > conceded:
            self.current["wins"] += 1
            opponent.current["losses"] += 1
            log_message(f"{self.name} won the match!")
            winner = self
        elif scored < conceded:
            opponent.current["wins"] += 1
            self.current["losses"] += 1
            log_message(f"{opponent.name} won the match!")
            winner = opponent
        else:
            if knockouts:
                winner, scored, conceded = handle_tie_breaking(scored, conceded)
            else:
                self.current["draws"] += 1
                opponent.current["draws"] += 1
                log_message(f"The match between {self.name} and {opponent.name} ended in a draw.")
                winner = "Draw"

        self.update_goals(opponent, scored, conceded)

        # Save log messages to file if specified
        if file:
            with open(file, 'a',  encoding="utf-8") as f:
                f.write('\n'.join(log_messages) + '\n')

        if return_all_info:
            return self.name, opponent.name, scored, conceded
        else:
            return winner

    def update_current(self):
        """Updates current season's statistics into cumulative stats."""
        self.wins += self.current["wins"]
        self.draws += self.current["draws"]
        self.losses += self.current["losses"]
        self.current["matches"] = self.current["wins"] + self.current["draws"] + self.current["losses"]
        self.matches_played += self.current["matches"]
        self.current["points"] = 3 * self.current["wins"] + self.current["draws"]
        self.points += self.current["points"]
        self.goals_scored += self.current["scored"]
        self.goals_against += self.current["against"]