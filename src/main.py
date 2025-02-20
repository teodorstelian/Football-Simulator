import sys

import settings
from database import get_best_teams, create_general_table, generate_teams_table, check_team_stats, \
    get_teams, update_team, get_competition_winners_from_db, create_european_competitions_table, \
    get_european_competition_stats, update_general_table_with_stats, populate_general_table, get_teams_by_skills
from leagues import league_simulation, select_league, select_teams_from_league, cup_simulation
from src.database import update_european_competition_appereances
from src.matches import play_european_cup


class MainProgram:
    def __init__(self):
        self.choice = None
        self.league = None
        self.europe_places = None
        self.teams_name = []
        self.teams_obj = []

    def run(self):
        while True:
            self.select_league_and_teams()
            self.select_choice()
            if self.choice.lower() == "q":  # Exit choice
                print("Thank you for using the program. Goodbye!")
                sys.exit(0)  # Gracefully exit

    def select_league_and_teams(self):
        """
        Allows the user to choose an action, along with the league and teams if required.
        """
        print(
            "1. Simulate a season \n"
            "2. Simulate a league \n"
            "3. Simulate a cup \n"
            "4. Simulate an European Cup \n"
            "5. Check best teams \n"
            "6. See stats for a team \n"
            "7. See most winners of a competition \n"
            "8. View European Competition Stats \n" 
            "9. See most skilled teams \n"
        )  # Menu options
        self.choice = input("Select action: ").strip()

        # Actions that do not require league or team selection
        no_team_selection = ["1", "4", "7", "8", "9", "q"]

        if self.choice not in no_team_selection:
            # Prompt user to select a league
            country = select_league()  # `select_league` prompts users to choose a league

            # Retrieve league and teams data based on the selected country
            self.league, self.teams_obj, self.teams_name, self.europe_places = select_teams_from_league(country)

            # Generate teams table for the selected league
            generate_teams_table(self.league, self.teams_obj)

        # Call method to update or create the general table
        self.update_general(create=True)

    def update_general(self, create=False):
        if create:
            print("Initializing general table and European tables...")
            self.initialize_european_tables()
            create_general_table()
            for country in settings.ALL_COUNTRIES:
                self.league, self.teams_obj, self.teams_name, self.europe_places = select_teams_from_league(country)
                generate_teams_table(self.league, self.teams_obj)
            populate_general_table()
        print("Updating general table with fresh stats...")
        update_general_table_with_stats()

    def update_all_leagues(self):
        for country in settings.ALL_COUNTRIES:
            for team in self.teams_obj:
                if team.country == country["name"]:
                    update_team(team, country["name"])  # Update team data in the database

    def simulate_season(self):
        """Simulates a season by playing all leagues and all european"""
        for country in settings.ALL_COUNTRIES:
            self.league, self.teams_obj, self.teams_name, self.europe_places = select_teams_from_league(country)
            generate_teams_table(self.league, self.teams_obj)
            self.simulate_league()
            self.simulate_cup()
        self.simulate_european(all_comps=True)

    def simulate_league(self):
        """Simulate a league"""
        self.teams_obj = league_simulation(self.league, self.teams_obj, self.europe_places)
        self.update_general()

    def simulate_cup(self):
        """Simulate a cup"""
        self.teams_obj = cup_simulation(self.league, self.teams_obj)
        self.update_general()

    def simulate_european(self, all_comps=False):
        if not all_comps:
            print("1. Champions League \n"
                  "2. Europa League \n"
                  "3. Europa Conference League \n")
            cup = input("Select competition:")
            competition = {
                "1": settings.UCL,
                "2": settings.UEL,
                "3": settings.UECL,
            }.get(cup)
            if competition is None:
                return
            # Include both Round 1 and Round 2 teams
            self.teams_obj = get_teams(european_cup=competition, rounds=["Round 1", "Round 2"])

            for team in self.teams_obj:
              # Track appearances for all teams
              update_european_competition_appereances(team.name, competition)

            self.teams_obj = play_european_cup(self.teams_obj, competition)

            self.update_general()
            self.update_all_leagues()
        else:
            for competition in [settings.UCL, settings.UEL, settings.UECL]:
                # Include both Round 1 and Round 2 teams
                self.teams_obj = get_teams(european_cup=competition, rounds=["Round 1", "Round 2"])

                for team in self.teams_obj:
                    update_european_competition_appereances(team.name, competition)

                self.teams_obj = play_european_cup(self.teams_obj, competition)

                self.update_general()
                self.update_all_leagues()

    def initialize_european_tables(self):
        for competition in [settings.UCL, settings.UEL, settings.UECL]:
            create_european_competitions_table(competition)

    def check_team_stats(self):
        """
            Check the stats of a team
        """
        input_team = input("Select team: ")
        for team in self.teams_obj:
            if input_team == team.name:
                self.update_general()
                check_team_stats(team, self.league)

    def view_european_competition_stats(self):
        print("1. Champions League \n"
              "2. Europa League \n"
              "3. Europa Conference League \n")
        cup = input("Select competition:")
        competition = {
            "1": settings.UCL,
            "2": settings.UEL,
            "3": settings.UECL,
        }.get(cup)
        if competition is None:
            print("Invalid selection.")
            return

        # Fetch and display stats including finals appearances
        stats = get_european_competition_stats(
            competition)

    def most_winners_by_competition(self):
        """
        Displays the teams with the most wins for a specific competition.
        """
        competition = input(
            "Enter the name of the competition (e.g., 'league_titles', 'cup_titles', 'ucl', 'uel', 'uecl'): ").strip()

        # Fetch competition winners from the database
        winners = get_competition_winners_from_db(competition)

        if not winners:
            print(f"No winners found or invalid competition: {competition}")
            return

        print(f"--- Teams with Most {competition.replace('_', ' ').title()} ---")
        for rank, (team, titles) in enumerate(winners, start=1):
            print(f"{rank}. {team}: {titles} titles")

    def get_best_skills_teams(self):
        """
        Retrieves and prints the best teams sorted by skill from the general table.
        """
        # Fetch the teams sorted by skill
        sorted_teams = get_teams_by_skills()

        if not sorted_teams:
            print("No teams are available based on skills.")
            return

    def select_choice(self):
        if self.choice == "1":
            self.simulate_season()
        if self.choice == "2":
            self.simulate_league()
        if self.choice == "3":
            self.simulate_cup()
        if self.choice == "4":
            self.simulate_european()
        if self.choice == "5":
            get_best_teams(self.league)
        if self.choice == "6":
            self.check_team_stats()
        if self.choice == "7":
            self.most_winners_by_competition()
        if self.choice == "8":
            self.view_european_competition_stats()
        if self.choice == "9":
            self.get_best_skills_teams()

if __name__ == "__main__":
    program = MainProgram()
    program.run()
