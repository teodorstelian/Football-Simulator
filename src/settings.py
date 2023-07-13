from src.all_teams import *

# Databases + Tables
COMPETITIONS_DB = "Competitions.db"
GENERAL_TABLE = "General"

# Countries - Name, Teams, European Places
ENG = {"name": "England",
       "teams": ENG_TEAMS,
       "europe": [3, 3, 3]}
ESP = {"name": "Spain",
       "teams": ESP_TEAMS,
       "europe": [3, 3, 3]}
GER = {"name": "Germany",
       "teams": GER_TEAMS,
       "europe": [3, 3, 3]}
ITA = {"name": "Italy",
       "teams": ITA_TEAMS,
       "europe": [3, 3, 3]}
FRA = {"name": "France",
       "teams": FRA_TEAMS,
       "europe": [2, 2, 2]}
NED = {"name": "Netherlands",
       "teams": NED_TEAMS,
       "europe": [1, 1, 1]}
POR = {"name": "Portugal",
       "teams": POR_TEAMS,
       "europe": [1, 1, 1]}

ALL_COUNTRIES = [ENG, ESP, GER, ITA, FRA, NED, POR]

# Europe Places - UCL, UEL, UECL
UCL = "Champions League"
UEL = "Europa League"
UECL = "Europa Conference League"
