import pytest
from src.team import Team
from unittest.mock import patch


# Mock settings module values
@pytest.fixture
def mock_settings():
    class MockSettings:
        AVG_BASE_GOALS = 1.5
        HOME_WEIGHT = 0.5
        SKILL_WEIGHT = 10

    return MockSettings()


# Test Team Initialization
def test_team_initialization():
    team = Team(name="Team A", country="Country A", skill=85)
    assert team.name == "Team A"
    assert team.country == "Country A"
    assert team.skill == 85
    assert team.points == 0
    assert team.matches_played == 0
    assert team.goals_scored == 0
    assert team.goals_against == 0


# Test update_goals
def test_update_goals():
    team1 = Team(name="Team A", country="Country A", skill=85)
    team2 = Team(name="Team B", country="Country B", skill=90)

    team1.update_goals(opponent=team2, scored=3, conceded=2)
    assert team1.current["scored"] == 3
    assert team1.current["against"] == 2
    assert team2.current["scored"] == 2
    assert team2.current["against"] == 3


# Test determine_match_outcome
def test_determine_match_outcome():
    team1 = Team(name="Team A", country="Country A", skill=85)
    team2 = Team(name="Team B", country="Country B", skill=90)

    assert team1.determine_match_outcome(3, 2, team2) == team1
    assert team1.current["wins"] == 1
    assert team2.current["wins"] == 0
    assert team2.current["losses"] == 1
    assert team1.current["losses"] == 0

    assert team1.determine_match_outcome(2, 3, team2) == team2
    assert team2.current["wins"] == 1
    assert team1.current["wins"] == 1
    assert team1.current["losses"] == 1
    assert team2.current["losses"] == 1

    assert team1.determine_match_outcome(2, 2, team2) == "Draw"


# Test calculate_goals with mock settings
def test_calculate_goals(mock_settings):
    with patch("src.settings", mock_settings):
        goals = Team.calculate_goals(85, 80, is_home=True)
        assert goals >= 0
        assert isinstance(goals, int)


# Test play_match (single leg)
def test_play_match_single_leg(mock_settings):
    with patch("src.settings", mock_settings):
        team1 = Team(name="Team A", country="Country A", skill=85)
        team2 = Team(name="Team B", country="Country B", skill=90)

        winner = team1.play_match(opponent=team2, knockouts=False)
        assert winner in [team1, team2, "Draw"]
        assert team1.current["scored"] >= 0
        assert team2.current["scored"] >= 0


# Test play_match (knockout with single leg)
def test_play_match_knockout_single_leg(mock_settings):
    with patch("src.settings", mock_settings):
        team1 = Team(name="Team A", country="Country A", skill=85)
        team2 = Team(name="Team B", country="Country B", skill=90)

        winner = team1.play_match(opponent=team2, knockouts=True)
        assert winner in [team1, team2]
        assert team1.current["scored"] >= 0
        assert team2.current["scored"] >= 0


# Test play_match (two legs)
def test_play_match_two_legs(mock_settings):
    with patch("src.settings", mock_settings):
        team1 = Team(name="Team A", country="Country A", skill=85)
        team2 = Team(name="Team B", country="Country B", skill=90)

        winner = team1.play_match(opponent=team2, knockouts=True, has_2_legs=True)
        assert winner in [team1, team2]
        assert team1.current["scored"] >= 0
        assert team2.current["scored"] >= 0


# Test update_current
def test_update_current():
    team = Team(name="Team A", country="Country A", skill=85)
    team.current["wins"] = 5
    team.current["draws"] = 3
    team.current["losses"] = 2
    team.current["scored"] = 20
    team.current["against"] = 15

    team.update_current()
    assert team.wins == 5
    assert team.draws == 3
    assert team.losses == 2
    assert team.points == (5 * 3 + 3)  # 3 points per win, 1 per draw
    assert team.matches_played == 10
    assert team.goals_scored == 20
    assert team.goals_against == 15
