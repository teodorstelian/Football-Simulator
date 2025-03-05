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
    "Ireland": 30,
    "Iceland": 31,
    "Kazakhstan": 32,
    "Israel": 33,
    "Cyprus": 34,
    "Belarus": 35,
    "Latvia": 36,
    "Lithuania": 37,
    "Estonia": 38,
    "Luxembourg": 39,
    "Georgia": 40,
    "Albania": 41,
    "Armenia": 42,
    "North_Macedonia": 43,
    "Kosovo": 44,
    "Moldova": 45,
    "Montenegro": 46,
    "Andorra": 47,
    "Malta": 48,
    "San_Marino": 49,
    "Liechtenstein": 50,
    "Faroe_Islands": 51,
}

FIRST_DIVISION_TEAM_COUNTS = {
    "England": 20,
    "Spain": 20,
    "Germany": 18,
    "Italy": 20,
    "France": 20,
    "Netherlands": 18,
    "Portugal": 18,
    "Belgium": 18,
    "Scotland": 12,
    "Austria": 12,
    "Romania": 16,
    "Switzerland": 10,
    "Turkey": 20,
    "Greece": 14,
    "Czech_Republic": 16,
    "Poland": 18,
    "Russia": 16,
    "Ukraine": 16,
    "Serbia": 16,
    "Norway": 16,
    "Sweden": 16,
    "Denmark": 12,
    "Hungary": 12,
    "Croatia": 12,
    "Bulgaria": 14,
    "Slovakia": 12,
    "Slovenia": 10,
    "Finland": 12,
    "Bosnia_and_Herzegovina": 12,
    "Ireland": 10,
    "Iceland": 12,
    "Kazakhstan": 14,
    "Israel": 14,
    "Cyprus": 14,
    "Belarus": 14,
    "Latvia": 10,
    "Lithuania": 10,
    "Estonia": 10,
    "Luxembourg": 8,
    "Georgia": 10,
    "Albania": 10,
    "Armenia": 10,
    "North_Macedonia": 10,
    "Kosovo": 10,
    "Moldova": 10,
    "Montenegro": 10,
    "Andorra": 8,
    "Malta": 12,
    "San_Marino": 10,
    "Liechtenstein": 8,
    "Faroe_Islands": 10,
}


# European Spots By Rank Ranges
EUROPE_PLACES_BY_RANK = {
    range(1, 2): {"UCL": [2, 1, 1], "UEL": [0, 2, 2], "UECL": [2, 1, 1]},  # Top Country
    range(2, 4): {"UCL": [1, 2, 1], "UEL": [0, 2, 1], "UECL": [1, 2, 0]},  # Ranks 2-3
    range(4, 6): {"UCL": [0, 3, 1], "UEL": [2, 1, 0], "UECL": [0, 2, 1]},  # Ranks 4-5
    range(6, 11): {"UCL": [0, 2, 1], "UEL": [0, 1, 2], "UECL": [0, 2, 1]},  # Ranks 6-10
    range(11, 16): {"UCL": [0, 1, 2], "UEL": [0, 1, 2], "UECL": [0, 1, 2]},  # Ranks 11-15
    range(16, 20): {"UCL": [0, 1, 1], "UEL": [0, 1, 2], "UECL": [0, 1, 2]},  # Ranks 15-19
    range(20, 22): {"UCL": [0, 1, 1], "UEL": [0, 1, 1], "UECL": [0, 1, 1]},  # Ranks 20-21
    range(22, 24): {"UCL": [0, 0, 2], "UEL": [0, 1, 1], "UECL": [0, 1, 1]},  # Ranks 22-23
    range(24, 30): {"UCL": [0, 0, 2], "UEL": [0, 1, 1], "UECL": [0, 0, 2]},  # Ranks 24-29
    range(30, 52): {"UCL": [0, 0, 1], "UEL": [0, 0, 1], "UECL": [0, 0, 1]},  # Ranks 30-51
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
    "Ireland": IRL_TEAMS,
    "Iceland": ICE_TEAMS,
    "Kazakhstan": KAZ_TEAMS,
    "Israel": ISR_TEAMS,
    "Cyprus": CYP_TEAMS,
    "Belarus": BLR_TEAMS,
    "Latvia": LAT_TEAMS,
    "Lithuania": LTU_TEAMS,
    "Estonia": EST_TEAMS,
    "Luxembourg": LUX_TEAMS,
    "Georgia": GEO_TEAMS,
    "Albania": ALB_TEAMS,
    "Armenia": ARM_TEAMS,
    "North_Macedonia": MKD_TEAMS,
    "Kosovo": KOS_TEAMS,
    "Moldova": MDA_TEAMS,
    "Montenegro": MNE_TEAMS,
    "Andorra": AND_TEAMS,
    "Malta": MLT_TEAMS,
    "San_Marino": SMR_TEAMS,
    "Liechtenstein": LIE_TEAMS,
    "Faroe_Islands": FRO_TEAMS,
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
        "first_division_teams": FIRST_DIVISION_TEAM_COUNTS.get(country_name, 12),
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
