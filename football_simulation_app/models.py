from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    skill = models.IntegerField()
    logo = models.ImageField(upload_to='team_logos/', null=True, blank=True)
    league_titles = models.IntegerField(default=0)
    cup_titles = models.IntegerField(default=0)
    ucl = models.IntegerField(default=0)
    uel = models.IntegerField(default=0)
    uecl = models.IntegerField(default=0)
    europe = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name


class LeagueTeam(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    league = models.CharField(max_length=255)
    matches_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    goals_scored = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.team.name} - {self.league}"


class GeneralTeam(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE, primary_key=True)
    matches_played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    goals_scored = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)

    def __str__(self):
        return self.team.name