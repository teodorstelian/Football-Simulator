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
       "europe": {"UCL": [2, 4], "UEL": [1, 2], "UECL": [2, 4]}}

ESP = {"name": "Spain",
       "teams": ESP_TEAMS,
       "europe": {"UCL": [2, 4], "UEL": [1, 2], "UECL": [1, 2]}}

GER = {"name": "Germany",
       "teams": GER_TEAMS,
       "europe": {"UCL": [2, 4], "UEL": [2, 4], "UECL": [1, 2]}}

ITA = {"name": "Italy",
       "teams": ITA_TEAMS,
       "europe": {"UCL": [2, 4], "UEL": [2, 4], "UECL": [1, 2]}}

FRA = {"name": "France",
       "teams": FRA_TEAMS,
       "europe": {"UCL": [2, 4], "UEL": [2, 4], "UECL": [1, 2]}}

NED = {"name": "Netherlands",
       "teams": NED_TEAMS,
        "europe": {"UCL": [1, 2], "UEL": [2, 4], "UECL": [1, 2]}}

POR = {"name": "Portugal",
       "teams": POR_TEAMS,
       "europe": {"UCL": [1, 2], "UEL": [2, 4], "UECL": [1, 2]}}

BEL = {"name": "Belgium",
       "teams": BEL_TEAMS,
       "europe": {"UCL": [1, 2], "UEL": [1, 2], "UECL": [2, 4]}}

SCO = {"name": "Scotland",
       "teams": SCO_TEAMS,
       "europe": {"UCL": [1, 2], "UEL": [1, 2], "UECL": [2, 4]}}

AUS = {"name": "Austria",
       "teams": AUS_TEAMS,
       "europe": {"UCL": [1, 2], "UEL": [1, 2], "UECL": [2, 4]}}

ROM = {"name": "Romania",
       "teams": ROM_TEAMS,
       "europe": {"UCL": [1, 2], "UEL": [1, 2], "UECL": [2, 4]}}

ALL_COUNTRIES = [ENG, ESP, GER, ITA, FRA, NED, POR, BEL, SCO, AUS, ROM]

# Europe Places - UCL, UEL, UECL
UCL = "Champions League"
UEL = "Europa League"
UECL = "Europa Conference League"
