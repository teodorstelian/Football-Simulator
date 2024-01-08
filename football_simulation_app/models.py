from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ucl_places = models.IntegerField(default=0)
    uel_places = models.IntegerField(default=0)
    uecl_places = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Countries"
    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    skill = models.IntegerField()
    logo = models.ImageField(null=True, blank=True)
    league_titles = models.IntegerField(default=0)
    cup_titles = models.IntegerField(default=0)
    ucl = models.IntegerField(default=0)
    uel = models.IntegerField(default=0)
    uecl = models.IntegerField(default=0)
    europe = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    age = models.IntegerField()
    skill = models.IntegerField()
    main_positions = models.CharField(max_length=255)
    secondary_positions = models.CharField(max_length=255, null=True, blank=True)
    tertiary_positions = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

# class LeagueTeam(models.Model):
#     team = models.ForeignKey(Team, on_delete=models.CASCADE)
#     league = models.CharField(max_length=255)
#     matches_played = models.IntegerField(default=0)
#     wins = models.IntegerField(default=0)
#     draws = models.IntegerField(default=0)
#     losses = models.IntegerField(default=0)
#     points = models.IntegerField(default=0)
#     goals_scored = models.IntegerField(default=0)
#     goals_against = models.IntegerField(default=0)
#
#     def __str__(self):
#         return f"{self.team.name} - {self.league}"
#
#
# class GeneralTeam(models.Model):
#     team = models.OneToOneField(Team, on_delete=models.CASCADE, primary_key=True)
#     matches_played = models.IntegerField(default=0)
#     wins = models.IntegerField(default=0)
#     draws = models.IntegerField(default=0)
#     losses = models.IntegerField(default=0)
#     points = models.IntegerField(default=0)
#     goals_scored = models.IntegerField(default=0)
#     goals_against = models.IntegerField(default=0)
#
#     def __str__(self):
#         return self.team.name