import settings
from database import get_best_teams, update_general_table, create_general_table, generate_teams_table, check_team_stats, \
    get_teams, update_team
from leagues import league_simulation, select_league, select_teams_from_league, cup_simulation
from src.matches import play_european_cup


class MainProgram:
    def __init__(self):
        # Initialize any variables or resources needed
        self.choice = None
        self.league = None
        self.europe_places = None
        self.teams_name = []
        self.teams_obj = []

    def run(self):
        while True:
            self.select_league_and_teams()
            self.select_choice()
            self.update_general(create=True)

    def select_league_and_teams(self):
        print("1. Simulate a season \n"
              "2. Simulate a league \n"
              "3. Simulate a cup \n"
              "4. Simulate an European Cup \n"
              "5. Check best teams \n"
              "6. See stats for a team \n"
              )
        self.choice = input("Select action: ")
        no_selection = ["1", "4"]
        if self.choice not in no_selection:
            country = select_league()
            self.league, self.teams_obj, self.teams_name, self.europe_places = select_teams_from_league(country)
            generate_teams_table(self.league, self.teams_obj)
        self.update_general(create=True)

    def update_general(self, create=False):
        if create:
            create_general_table()
        for team in self.teams_obj:
            update_general_table(team)

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
        """
            Simulate a european cup
        :param all_comps: If True, simulate all cups
        """
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
            self.teams_obj = get_teams(european_cup=competition)
            self.teams_obj = play_european_cup(self.teams_obj, competition)
            self.update_general()
            self.update_all_leagues()
        else:
            for competition in [settings.UECL, settings.UEL, settings.UCL]:
                self.teams_obj = get_teams(european_cup=competition)
                self.teams_obj = play_european_cup(self.teams_obj, competition)
                self.update_general()
                self.update_all_leagues()

    def check_team_stats(self):
        """
            Check the stats of a team
        """
        input_team = input("Select team: ")
        for team in self.teams_obj:
            if input_team == team.name:
                self.update_general()
                check_team_stats(team, self.league)

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


if __name__ == "__main__":
    program = MainProgram()
    program.run()
