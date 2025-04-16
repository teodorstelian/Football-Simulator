import pytest

from src.settings import ALL_COUNTRIES


def calculate_teams_by_round(competition_name):
    """
    Helper function to calculate teams for each round for a given competition.
    Splits counts into first and second round.

    :param competition_name: The name of the European competition (UCL, UEL, UECL)
    :return: A tuple with total teams in (first_round, second_round)
    """
    first_round_teams = 0
    second_round_teams = 0
    third_round_teams = 0
    play_off_teams = 0
    league_phase_teams = 0

    for country in ALL_COUNTRIES:
        europe_places = country.get("europe", {})
        if competition_name in europe_places:
            # Add the number of teams for each round
            league_phase_teams += europe_places[competition_name][0]
            play_off_teams += europe_places[competition_name][1]
            third_round_teams += europe_places[competition_name][2]
            second_round_teams += europe_places[competition_name][3]
            first_round_teams += europe_places[competition_name][4]

    return first_round_teams, second_round_teams, third_round_teams, play_off_teams, league_phase_teams

@pytest.mark.parametrize("competition, expected_league_phase, expected_play_off, expected_third_round, expected_second_round, expected_first_round", [
    ("UCL", 12, 28, 24, 16, 32),
    ("UEL", 12, 28, 24, 16, 32),
    ("UECL", 12, 28, 24, 16, 32),
])
def test_teams_by_round(competition, expected_league_phase, expected_play_off, expected_third_round, expected_second_round, expected_first_round):
    """Test the distribution of teams for given competition by rounds."""
    first_round, second_round, third_round, play_off_round, league_phase = calculate_teams_by_round(competition)
    print(f"{competition} - First Round: {first_round}, Second Round: {second_round},"
          f" Third Round: {third_round}, Play-Off: {play_off_round}, League Phase: {league_phase}")
    assert league_phase == expected_league_phase
    assert play_off_round == expected_play_off
    assert third_round == expected_third_round
    assert second_round == expected_second_round
    assert first_round == expected_first_round
    all_second = first_round / 2 + second_round
    assert all_second == 32
    all_third = all_second / 2 + third_round
    assert all_third == 40
    all_p_off = all_third / 2 + play_off_round
    assert all_p_off == 48
    all_league = league_phase + (all_p_off / 2)
    assert all_league == 36
