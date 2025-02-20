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
       "europe": {"UCL": [2, 4], "UEL": [0, 4], "UECL": [0, 4]}}

ESP = {"name": "Spain",
       "teams": ESP_TEAMS,
       "europe": {"UCL": [2, 4], "UEL": [0, 4], "UECL": [0, 4]}}

GER = {"name": "Germany",
       "teams": GER_TEAMS,
       "europe": {"UCL": [2, 4], "UEL": [0, 4], "UECL": [0, 4]}}

ITA = {"name": "Italy",
       "teams": ITA_TEAMS,
       "europe": {"UCL": [2, 4], "UEL": [0, 4], "UECL": [0, 4]}}

FRA = {"name": "France",
       "teams": FRA_TEAMS,
       "europe": {"UCL": [2, 4], "UEL": [0, 4], "UECL": [0, 4]}}

NED = {"name": "Netherlands",
       "teams": NED_TEAMS,
        "europe": {"UCL": [2, 4], "UEL": [2, 2], "UECL": [2, 2]}}

POR = {"name": "Portugal",
       "teams": POR_TEAMS,
       "europe": {"UCL": [2, 4], "UEL": [2, 2], "UECL": [2, 2]}}

BEL = {"name": "Belgium",
       "teams": BEL_TEAMS,
       "europe": {"UCL": [2, 4], "UEL": [1, 2], "UECL": [1, 2]}}

SCO = {"name": "Scotland",
       "teams": SCO_TEAMS,
       "europe": {"UCL": [2, 4], "UEL": [1, 2], "UECL": [1, 2]}}

AUS = {"name": "Austria",
       "teams": AUS_TEAMS,
       "europe": {"UCL": [2, 4], "UEL": [1, 2], "UECL": [1, 2]}}

ROM = {"name": "Romania",
       "teams": ROM_TEAMS,
       "europe": {"UCL": [2, 4], "UEL": [1, 2], "UECL": [1, 2]}}

SUI = {"name": "Switzerland",
       "teams": SUI_TEAMS,
       "europe": {"UCL": [2, 4], "UEL": [1, 0], "UECL": [1, 0]}}

TUR = {"name": "Turkey",
       "teams": TUR_TEAMS,
       "europe": {"UCL": [2, 4], "UEL": [1, 0], "UECL": [1, 0]}}

GRE = {"name": "Greece",
       "teams": GRE_TEAMS,
       "europe": {"UCL": [1, 2], "UEL": [1, 0], "UECL": [1, 0]}}

CZE = {"name": "Czech_Republic",
       "teams": CZE_TEAMS,
       "europe": {"UCL": [1, 2], "UEL": [1, 0], "UECL": [1, 0]}}

POL = {"name": "Poland",
       "teams": POL_TEAMS,
       "europe": {"UCL": [1, 2], "UEL": [1, 0], "UECL": [1, 0]}}

RUS = {"name": "Russia",
       "teams": RUS_TEAMS,
       "europe": {"UCL": [1, 2], "UEL": [1, 0], "UECL": [1, 0]}}

UKR = {"name": "Ukraine",
       "teams": UKR_TEAMS,
       "europe": {"UCL": [1, 2], "UEL": [1, 0], "UECL": [1, 0]}}

SRB = {"name": "Serbia",
       "teams": SRB_TEAMS,
       "europe": {"UCL": [1, 2], "UEL": [1, 0], "UECL": [1, 0]}}
ALL_COUNTRIES = [ENG, ESP, GER, ITA, FRA, NED, POR, BEL, SCO, AUS, ROM, SUI, TUR, GRE, CZE, POL, RUS, UKR, SRB]

# Europe Places - UCL, UEL, UECL
UCL = "Champions League"
UEL = "Europa League"
UECL = "Europa Conference League"
