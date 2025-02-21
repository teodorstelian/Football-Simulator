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
       "europe": {"UCL": [2, 3], "UEL": [1, 4], "UECL": [1, 4]}}

ESP = {"name": "Spain",
       "teams": ESP_TEAMS,
       "europe": {"UCL": [2, 3], "UEL": [1, 4], "UECL": [1, 4]}}

GER = {"name": "Germany",
       "teams": GER_TEAMS,
       "europe": {"UCL": [2, 3], "UEL": [1, 4], "UECL": [1, 4]}}

ITA = {"name": "Italy",
       "teams": ITA_TEAMS,
       "europe": {"UCL": [2, 3], "UEL": [1, 4], "UECL": [1, 4]}}

FRA = {"name": "France",
       "teams": FRA_TEAMS,
       "europe": {"UCL": [2, 3], "UEL": [1, 4], "UECL": [1, 4]}}

NED = {"name": "Netherlands",
       "teams": NED_TEAMS,
        "europe": {"UCL": [2, 2], "UEL": [2, 4], "UECL": [2, 4]}}

POR = {"name": "Portugal",
       "teams": POR_TEAMS,
       "europe": {"UCL": [2, 2], "UEL": [2, 4], "UECL": [2, 4]}}

BEL = {"name": "Belgium",
       "teams": BEL_TEAMS,
       "europe": {"UCL": [2, 2], "UEL": [1, 3], "UECL": [2, 2]}}

SCO = {"name": "Scotland",
       "teams": SCO_TEAMS,
       "europe": {"UCL": [2, 2], "UEL": [2, 2], "UECL": [1, 3]}}

AUS = {"name": "Austria",
       "teams": AUS_TEAMS,
       "europe": {"UCL": [2, 2], "UEL": [2, 2], "UECL": [2, 2]}}

ROM = {"name": "Romania",
       "teams": ROM_TEAMS,
       "europe": {"UCL": [2, 4], "UEL": [2, 2], "UECL": [2, 2]}}

SUI = {"name": "Switzerland",
       "teams": SUI_TEAMS,
       "europe": {"UCL": [2, 4], "UEL": [1, 2], "UECL": [1, 2]}}

TUR = {"name": "Turkey",
       "teams": TUR_TEAMS,
       "europe": {"UCL": [2, 4], "UEL": [1, 3], "UECL": [1, 3]}}

GRE = {"name": "Greece",
       "teams": GRE_TEAMS,
       "europe": {"UCL": [1, 2], "UEL": [1, 2], "UECL": [1, 2]}}

CZE = {"name": "Czech_Republic",
       "teams": CZE_TEAMS,
       "europe": {"UCL": [1, 2], "UEL": [1, 2], "UECL": [1, 2]}}

POL = {"name": "Poland",
       "teams": POL_TEAMS,
       "europe": {"UCL": [1, 2], "UEL": [1, 2], "UECL": [1, 2]}}

RUS = {"name": "Russia",
       "teams": RUS_TEAMS,
       "europe": {"UCL": [1, 2], "UEL": [1, 2], "UECL": [1, 2]}}

UKR = {"name": "Ukraine",
       "teams": UKR_TEAMS,
       "europe": {"UCL": [1, 2], "UEL": [1, 2], "UECL": [1, 2]}}

SRB = {"name": "Serbia",
       "teams": SRB_TEAMS,
       "europe": {"UCL": [1, 2], "UEL": [1, 2], "UECL": [1, 2]}}

NOR = {"name": "Norway",
       "teams": NOR_TEAMS,
       "europe": {"UCL": [0, 1], "UEL": [1, 1], "UECL": [1, 1]}}

SWE = {"name": "Sweden",
       "teams": SWE_TEAMS,
       "europe": {"UCL": [0, 1], "UEL": [1, 1], "UECL": [1, 1]}}

DEN = {"name": "Denmark",
       "teams": DEN_TEAMS,
       "europe": {"UCL": [0, 2], "UEL": [1, 1], "UECL": [1, 1]}}

HUN = {"name": "Hungary",
       "teams": HUN_TEAMS,
       "europe": {"UCL": [0, 2], "UEL": [1, 1], "UECL": [1, 1]}}

CRO = {"name": "Croatia",
       "teams": CRO_TEAMS,
       "europe": {"UCL": [0, 2], "UEL": [1, 1], "UECL": [1, 1]}}

BUL = {"name": "Bulgaria",
       "teams": BUL_TEAMS,
       "europe": {"UCL": [0, 2], "UEL": [1, 1], "UECL": [1, 1]}}

SVK = {"name": "Slovakia",
       "teams": SVK_TEAMS,
       "europe": {"UCL": [0, 1], "UEL": [1, 1], "UECL": [1, 1]}}

SLO = {"name": "Slovenia",
       "teams": SLO_TEAMS,
       "europe": {"UCL": [0, 1], "UEL": [1, 1], "UECL": [1, 1]}}

FIN = {"name": "Finland",
       "teams": FIN_TEAMS,
       "europe": {"UCL": [0, 2], "UEL": [0, 1], "UECL": [0, 1]}}

BIH = {"name": "Bosnia_and_Herzegovina",
       "teams": BIH_TEAMS,
       "europe": {"UCL": [0, 1], "UEL": [0, 1], "UECL": [0, 1]}}

ALL_COUNTRIES = [ENG, ESP, GER, ITA, FRA, NED, POR, BEL, SCO, AUS, ROM, SUI, TUR, GRE, CZE, POL,
                 RUS, UKR, SRB, NOR, SWE, DEN, HUN, CRO, BUL, SVK, SLO, FIN, BIH]

# European Competitions
UCL = "Champions League"
UEL = "Europa League"
UECL = "Europa Conference League"

# Match Variables
AVG_BASE_GOALS = 1.5
HOME_WEIGHT = 0.5
SKILL_WEIGHT = 15

# Limits
BEST_TEAMS_SKILLS = 25
BEST_TEAMS_LEAGUE = 10
