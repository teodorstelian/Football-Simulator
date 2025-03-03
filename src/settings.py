from src.all_teams import *

# Folders
RESULTS_FOLDER = "../results"
WINNERS_TEXT = "winners.txt"

# Databases + Tables
COMPETITIONS_DB = "Competitions.db"
GENERAL_TABLE = "General"

# Country Rankings (1 for the strongest, increasing for weaker countries)
COUNTRY_RANKINGS = {
    "England": 1,
    "Spain": 2,
    "Germany": 3,
    "Italy": 4,
    "France": 5,
    "Netherlands": 6,
    "Portugal": 7,
    "Belgium": 8,
    "Scotland": 9,
    "Austria": 10,
    "Romania": 11,
    "Switzerland": 12,
    "Turkey": 13,
    "Greece": 14,
    "Czech_Republic": 15,
    "Poland": 16,
    "Russia": 17,
    "Ukraine": 18,
    "Serbia": 19,
    "Norway": 20,
    "Sweden": 21,
    "Denmark": 22,
    "Hungary": 23,
    "Croatia": 24,
    "Bulgaria": 25,
    "Slovakia": 26,
    "Slovenia": 27,
    "Finland": 28,
    "Bosnia_and_Herzegovina": 29,
}

# European Spots By Rank Ranges
EUROPE_PLACES_BY_RANK = {
    range(1, 2): {"UCL": [2, 1, 2], "UEL": [0, 2, 2], "UECL": [2, 1, 2]},  # Top 3 countries
    range(2, 4): {"UCL": [1, 3, 2], "UEL": [0, 2, 1], "UECL": [1, 3, 2]},  # Top 3 countries
    range(4, 6): {"UCL": [0, 3, 2], "UEL": [2, 1, 1], "UECL": [0, 3, 2]},  # Top 3 countries
    range(6, 11): {"UCL": [0, 2, 3], "UEL": [0, 1, 3], "UECL": [0, 2, 3]},  # Ranks 5-6
    range(11, 16): {"UCL": [0, 1, 3], "UEL": [0, 1, 3], "UECL": [0, 1, 3]},  # Ranks 7-10
    range(16, 20): {"UCL": [0, 1, 2], "UEL": [0, 1, 2], "UECL": [0, 1, 2]},  # Ranks 11-20
    range(20, 26): {"UCL": [0, 0, 2], "UEL": [0, 1, 2], "UECL": [0, 0, 2]},  # Ranks 11-20
    range(26, 30): {"UCL": [0, 0, 1], "UEL": [0, 1, 2], "UECL": [0, 0, 1]},  # Ranks 11-20
}


TEAM_MAPPINGS = {
    "England": ENG_TEAMS,
    "Spain": ESP_TEAMS,
    "Germany": GER_TEAMS,
    "Italy": ITA_TEAMS,
    "France": FRA_TEAMS,
    "Netherlands": NED_TEAMS,
    "Portugal": POR_TEAMS,
    "Belgium": BEL_TEAMS,
    "Scotland": SCO_TEAMS,
    "Austria": AUS_TEAMS,
    "Romania": ROM_TEAMS,
    "Switzerland": SUI_TEAMS,
    "Turkey": TUR_TEAMS,
    "Greece": GRE_TEAMS,
    "Czech_Republic": CZE_TEAMS,
    "Poland": POL_TEAMS,
    "Russia": RUS_TEAMS,
    "Ukraine": UKR_TEAMS,
    "Serbia": SRB_TEAMS,
    "Norway": NOR_TEAMS,
    "Sweden": SWE_TEAMS,
    "Denmark": DEN_TEAMS,
    "Hungary": HUN_TEAMS,
    "Croatia": CRO_TEAMS,
    "Bulgaria": BUL_TEAMS,
    "Slovakia": SVK_TEAMS,
    "Slovenia": SLO_TEAMS,
    "Finland": FIN_TEAMS,
    "Bosnia_and_Herzegovina": BIH_TEAMS,
}


# Function to determine European places for a country based on its ranking
def get_europe_places(country_name):
    rank = COUNTRY_RANKINGS.get(country_name)
    if rank is None:
        raise ValueError(f"Country '{country_name}' is not ranked.")

    for rank_range, places in EUROPE_PLACES_BY_RANK.items():
        if rank in rank_range:
            return places

    # Default for unranked or unmatched countries
    return {"UCL": [0, 0, 0], "UEL": [0, 0, 0], "UECL": [0, 0, 0]}


# Generate ALL_COUNTRIES dynamically
ALL_COUNTRIES = []
for country_name in COUNTRY_RANKINGS:
    country_data = {
        "name": country_name,
        "teams": TEAM_MAPPINGS.get(country_name, []),  # Use defined teams or an empty list
        "europe": get_europe_places(country_name),  # Dynamically fetch Europe places
    }
    ALL_COUNTRIES.append(country_data)

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

# Coefficients
COEF_WIN = 60
COEF_FIN = 25
COEF_SEM = 12
COEF_QUA = 5.5
COEF_R16 = 2.7
COEF_R32 = 1.3
COEF_LGP = 0.6
COEF_QR2 = 0.25
COEF_QR1 = 0.1
