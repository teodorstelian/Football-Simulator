import settings


def select_league():
    print("1. Premier League \n"
          "2. La Liga \n"
          "3. Bundesliga \n"
          "4. Ligue 1 \n"
          "5. Serie A")
    league = input("Select the league: ")

    if league == '1':
        db = settings.ENG_DB
        teams = settings.ENG_TEAMS

    if league == '2':
        db = settings.ESP_DB
        teams = settings.ESP_TEAMS

    if league == '3':
        db = settings.GER_DB
        teams = settings.GER_TEAMS

    if league == '4':
        db = settings.FRA_DB
        teams = settings.FRA_TEAMS

    if league == '5':
        db = settings.ITA_DB
        teams = settings.ITA_TEAMS

    return db, teams
