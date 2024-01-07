from src.teams_data import *

# Folders
RESULTS_FOLDER = "results"
WINNERS_TEXT = "winners.txt"

# Databases + Tables
COMPETITIONS_DB = "Competitions.db"
GENERAL_TABLE = "General"

# Countries - Name, Teams, European Places
ENG = {"name": "England",
       "teams_logo": ENG_TEAMS,
       "europe": [4, 4, 4]}
ESP = {"name": "Spain",
       "teams_logo": ESP_TEAMS,
       "europe": [4, 4, 4]}
GER = {"name": "Germany",
       "teams_logo": GER_TEAMS,
       "europe": [4, 4, 4]}
ITA = {"name": "Italy",
       "teams_logo": ITA_TEAMS,
       "europe": [4, 4, 4]}
FRA = {"name": "France",
       "teams_logo": FRA_TEAMS,
       "europe": [4, 4, 4]}
NED = {"name": "Netherlands",
       "teams_logo": NED_TEAMS,
       "europe": [3, 3, 3]}
POR = {"name": "Portugal",
       "teams_logo": POR_TEAMS,
       "europe": [3, 3, 3]}

BEL = {"name": "Belgium",
       "teams_logo": BEL_TEAMS,
       "europe": [2, 2, 2]}

SCO = {"name": "Scotland",
       "teams_logo": SCO_TEAMS,
       "europe": [2, 2, 2]}

AUS = {"name": "Austria",
       "teams_logo": AUS_TEAMS,
       "europe": [2, 2, 2]}
ALL_COUNTRIES = [ENG, ESP, GER, ITA, FRA, NED, POR, BEL, SCO, AUS]

# Europe Places - UCL, UEL, UECL
UCL = "Champions League"
UEL = "Europa League"
UECL = "Europa Conference League"
