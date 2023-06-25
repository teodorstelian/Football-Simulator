import settings
from database import get_best_teams, update_general_table, create_general_table, generate_teams_table, check_team_stats, \
    get_european_teams
from european_cups import play_european_cup
from leagues import simulate_season, select_league


class MainProgram:
    def __init__(self):
        # Initialize any variables or resources needed
        self.choice = None
        self.league = None
        self.teams_name = []
        self.teams_obj = []

    def select_league_and_teams(self):
        print("1. Simulate a league \n"
              "2. Check best teams \n"
              "3. See stats for a team \n"
              "4. Simulate European Cup")
        self.choice = input("Select action: ")
        if self.choice != "4":
            self.league, self.teams_obj, self.teams_name = select_league()
            generate_teams_table(self.league, self.teams_obj)
        create_general_table()
        for team in self.teams_obj:
            update_general_table(team)

    def select_choice(self):
        if self.choice == "1":
            self.teams_obj = simulate_season(self.league, self.teams_obj)
            for team in self.teams_obj:
                update_general_table(team)
        if self.choice == "2":
            get_best_teams(self.league)
        if self.choice == "3":
            input_team = input("Select team: ")
            for team in self.teams_obj:
                if input_team == team.name:
                    update_general_table(team)
                    check_team_stats(team, self.league)
        if self.choice == "4":
            print("1. Champions League \n"
                  "2. Europa League \n"
                  "3. Europa Conference League \n")
            cup = input("Select competition:")
            if cup == "1":
                competition = settings.UCL
            elif cup == "2":
                competition = settings.UEL
            elif cup == "3":
                competition = settings.UECL
            else:
                return
            self.teams_obj = get_european_teams(competition)
            play_european_cup(self.teams_obj, competition)

    def run(self):
        while True:
            self.select_league_and_teams()
            self.select_choice()
            create_general_table()
            for team in self.teams_obj:
                update_general_table(team)


if __name__ == "__main__":
    program = MainProgram()
    program.run()
