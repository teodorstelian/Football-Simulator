from src.all_teams import *

# Folders
RESULTS_FOLDER = "../results"
WINNERS_TEXT = "winners.txt"

# Databases + Tables
COMPETITIONS_DB = "Competitions.db"
GENERAL_TABLE = "General"

# Countries - Name, Teams, European Places
ENG = {"name": "England",
       "teams": ENG_TEAMS,
       "europe": [4, 4, 4]}
ESP = {"name": "Spain",
       "teams": ESP_TEAMS,
       "europe": [4, 4, 4]}
GER = {"name": "Germany",
       "teams": GER_TEAMS,
       "europe": [4, 4, 4]}
ITA = {"name": "Italy",
       "teams": ITA_TEAMS,
       "europe": [4, 4, 4]}
FRA = {"name": "France",
       "teams": FRA_TEAMS,
       "europe": [4, 4, 4]}
NED = {"name": "Netherlands",
       "teams": NED_TEAMS,
       "europe": [3, 3, 3]}
POR = {"name": "Portugal",
       "teams": POR_TEAMS,
       "europe": [3, 3, 3]}

BEL = {"name": "Belgium",
       "teams": BEL_TEAMS,
       "europe": [2, 2, 2]}

SCO = {"name": "Scotland",
       "teams": SCO_TEAMS,
       "europe": [2, 2, 2]}

AUS = {"name": "Austria",
       "teams": AUS_TEAMS,
       "europe": [2, 2, 2]}
ALL_COUNTRIES = [ENG, ESP, GER, ITA, FRA, NED, POR, BEL, SCO, AUS]

# Europe Places - UCL, UEL, UECL
UCL = "Champions League"
UEL = "Europa League"
UECL = "Europa Conference League"
