import sys

from database import (
    create_general_table,
    update_general_table_with_stats,
    populate_general_table,
    generate_teams_table,
    get_teams,
    check_team_stats,
    get_best_teams_from_league,
    get_competition_winners_from_db,
    create_european_competitions_table,
    get_european_competition_stats,
    get_teams_by_skills,
)
from national_leagues import league_simulation, select_teams_from_league
from src.database import update_european_competition_appereances
from src.european_cups import play_european_cup
from src.national_cups import cup_simulation


class InputHandler:
    @staticmethod
    def display_main_menu():
        print(
            "1. Simulate a season\n"
            "2. Simulate a league\n"
            "3. Simulate a cup\n"
            "4. Simulate a European Cup\n"
            "5. Check best teams\n"
            "6. See stats for a team\n"
            "7. See most winners of a competition\n"
            "8. View European Competition Stats\n"
            "9. See most skilled teams\n"
            "q. Quit"
        )
        return input("Select action: ").strip().lower()

    @staticmethod
    def get_user_input(prompt):
        return input(prompt).strip()


class DatabaseUpdater:
    @staticmethod
    def initialize_database(settings):
        print("Initializing general table and European tables...")
        DatabaseUpdater.initialize_european_tables(settings)
        create_general_table()
        for country in settings.ALL_COUNTRIES:
            league, teams_obj, teams_name, europe_places = select_teams_from_league(country)
            generate_teams_table(league, teams_obj)
        populate_general_table()
        update_general_table_with_stats()

    @staticmethod
    def initialize_european_tables(settings):
        for competition in [settings.UCL, settings.UEL, settings.UECL]:
            create_european_competitions_table(competition)

    @staticmethod
    def update_general():
        print("Updating general table with fresh stats...")
        update_general_table_with_stats()

class LeagueSimulator:
    @classmethod
    def simulate_league(cls, league, teams_obj, europe_places):
        return league_simulation(league, teams_obj, europe_places)


class CupSimulator:
    @classmethod
    def simulate_cup(cls, league, teams_obj):
        return cup_simulation(league, teams_obj)


class EuropeanCupSimulator:
    @classmethod
    def simulate_european_cup(cls, competition):
        teams = get_teams(european_cup=competition, rounds=["Round 1", "Round 2"])
        for team in teams:
            update_european_competition_appereances(team.name, competition)
        return play_european_cup(teams, competition)


class StatsViewer:
    @staticmethod
    def get_competition_winners(competition):
        winners = get_competition_winners_from_db(competition)
        if not winners:
            print(f"No winners found for competition: {competition}")
            return
        for rank, (team, titles) in enumerate(winners, start=1):
            print(f"{rank}. {team}: {titles} titles")

class MainProgram:
    def __init__(self, settings):
        self.settings = settings
        self.league = None
        self.teams_obj = []
        self.teams_name = []
        self.europe_places = None
        self.choice = None

        # Initialize dependencies
        self.input_handler = InputHandler()
        self.db_updater = DatabaseUpdater()
        self.stats_viewer = StatsViewer()
        self.european_simulator = EuropeanCupSimulator()

    def run(self):
        self.db_updater.initialize_database(self.settings)
        while True:
            self.choice = self.input_handler.display_main_menu()
            if self.choice == "q":
                print("Thank you for using the program. Goodbye!")
                sys.exit(0)
            self.handle_choice()

    def handle_choice(self):
        actions = {
            "1": self.simulate_season,
            "2": self.simulate_league,
            "3": self.simulate_cup,
            "4": self.simulate_european,
            "5": self.view_best_teams,
            "6": self.view_team_stats,
            "7": self.view_winners,
            "8": self.view_european_stats,
            "9": get_teams_by_skills,
        }
        if action := actions.get(self.choice):
            action()
        else:
            print("Invalid choice. Please try again.")


    def simulate_season(self):
        """Simulates an entire season: league → cup → all European competitions."""
        seasons = int(self.input_handler.get_user_input("Enter number of seasons: "))
        for _ in range(seasons):
            for country in self.settings.ALL_COUNTRIES:
                self.league, self.teams_obj, self.teams_name, self.europe_places = select_teams_from_league(country)
                self.teams_obj = LeagueSimulator.simulate_league(self.league, self.teams_obj, self.europe_places)
                self.db_updater.update_general()
                self.teams_obj = CupSimulator.simulate_cup(self.league, self.teams_obj)
                self.db_updater.update_general()

            for competition in [self.settings.UCL, self.settings.UEL, self.settings.UECL]:
                self.teams_obj = EuropeanCupSimulator.simulate_european_cup(competition)
                self.db_updater.update_general()

    def simulate_league(self):
        country_name = self.input_handler.get_user_input("Enter the country name: ")

        selected_country = next(
            (country for country in self.settings.ALL_COUNTRIES if country["name"].lower() == country_name.lower()),
            None
        )
        if not selected_country:
            print(f"No league found for the specified country: {country_name}")
            return

        self.league, self.teams_obj, self.teams_name, self.europe_places = select_teams_from_league(selected_country)

        self.teams_obj = LeagueSimulator.simulate_league(self.league, self.teams_obj, self.europe_places)
        self.db_updater.update_general()
        print(f"League simulation for {country_name} has been completed.")

    def simulate_cup(self):
        country_name = self.input_handler.get_user_input("Enter the country name: ")

        selected_country = next(
            (country for country in self.settings.ALL_COUNTRIES if country["name"].lower() == country_name.lower()),
            None
        )
        if not selected_country:
            print(f"No cup found for the specified country: {country_name}")
            return

        self.league, self.teams_obj, self.teams_name, self.europe_places = select_teams_from_league(selected_country)

        self.teams_obj = CupSimulator.simulate_cup(self.league, self.teams_obj)
        self.db_updater.update_general()
        print(f"Cup simulation for {country_name} has been completed.")

    def simulate_european(self):
        competitions = {"1": self.settings.UCL, "2": self.settings.UEL, "3": self.settings.UECL}
        choice = self.input_handler.get_user_input(
            "Select competition (1. Champions League, 2. Europa League, 3. Europa Conference League): "
        )
        if competition := competitions.get(choice):
            self.teams_obj = EuropeanCupSimulator.simulate_european_cup(competition)
            self.db_updater.update_general()

    def view_best_teams(self):
        country_name = self.input_handler.get_user_input("Enter the country name: ")

        selected_country = next(
            (country for country in self.settings.ALL_COUNTRIES if country["name"].lower() == country_name.lower()),
            None
        )
        if not selected_country:
            print(f"No league found for the specified country: {country_name}")
            return

        get_best_teams_from_league(selected_country["name"])

    def view_team_stats(self):
        country_name = self.input_handler.get_user_input("Enter the country name: ")

        selected_country = next(
            (country for country in self.settings.ALL_COUNTRIES if country["name"].lower() == country_name.lower()),
            None
        )
        if not selected_country:
            print(f"No cup found for the specified country: {country_name}")
            return

        self.league, self.teams_obj, self.teams_name, self.europe_places = select_teams_from_league(selected_country)
        team_name = self.input_handler.get_user_input("Enter team name: ")
        for team in self.teams_obj:
            if team.name == team_name:
                check_team_stats(team, self.league)

    def view_winners(self):
        competition = self.input_handler.get_user_input("Enter competition name: ")
        self.stats_viewer.get_competition_winners(competition)

    def view_european_stats(self):
        competition = self.input_handler.get_user_input(
            "Select competition (1. UCL, 2. UEL, 3. UECL): "
        )
        competitions = {"1": self.settings.UCL, "2": self.settings.UEL, "3": self.settings.UECL}
        get_european_competition_stats(competitions.get(competition))


if __name__ == "__main__":
    from importlib import import_module

    settings = import_module("settings")
    program = MainProgram(settings)
    program.run()
