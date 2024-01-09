from pathlib import Path

from django.db import models
from django.db.models import Q

from src.initial_data import DEFENSE_POSITIONS, MIDFIELD_POSITIONS, ATTACK_POSITIONS, POSITIONS


class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)
    ucl_places = models.IntegerField(default=0)
    uel_places = models.IntegerField(default=0)
    uecl_places = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Countries"
    def __str__(self):
        return self.name

def team_logo_path(instance):
    if not instance.name:
        return "teams_logo/default.png"
    photo_path = Path(f"teams_logo/{instance.country}/{instance.name}.png")
    return (
        str(photo_path)
        if photo_path.exists()
        else "teams_logo/default.png"
    )

class Team(models.Model):
    name = models.CharField(max_length=255)
    id = models.IntegerField(primary_key=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    skill = models.IntegerField(default=0)
    logo = models.ImageField(null=True, blank=True)
    league_titles = models.IntegerField(default=0)
    cup_titles = models.IntegerField(default=0)
    ucl = models.IntegerField(default=0)
    uel = models.IntegerField(default=0)
    uecl = models.IntegerField(default=0)
    europe = models.CharField(max_length=255, blank=True)

    defense_skill = models.FloatField(null=True, default=0)
    midfield_skill = models.FloatField(null=True, default=0)
    attack_skill = models.FloatField(null=True, default=0)

    def calculate_average_skill(self, positions):
        filter_conditions = Q()
        for position in positions:
            filter_conditions |= Q(main_position__contains=[position])
            # Filter players based on team ID and the conditions
        players = Player.objects.filter(team=self.id).filter(filter_conditions)
        #breakpoint()
        if players is None:
            return 0
        total_skill = sum(player.skill for player in players)
        num_players = len(players)
        average_skill = round(total_skill / num_players,1) if num_players > 0 else 0
        print(f"Team: {self.name}, Positions: {positions}, Average Skill: {average_skill}")
        return average_skill

    def calculate_average_defense_skill(self):
        return self.calculate_average_skill(DEFENSE_POSITIONS)

    def calculate_average_midfield_skill(self):
        return self.calculate_average_skill(MIDFIELD_POSITIONS)

    def calculate_average_attack_skill(self):
        return self.calculate_average_skill(ATTACK_POSITIONS)

    def save(self, *args, **kwargs):
        self.skill = self.calculate_average_skill(POSITIONS)
        self.defense_skill = self.calculate_average_defense_skill()
        self.midfield_skill = self.calculate_average_midfield_skill()
        self.attack_skill = self.calculate_average_attack_skill()
        self.logo = team_logo_path(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

def player_photo_path(instance):
    if not instance.name:
        return "players_photo/default.png"
    photo_path = Path(f"players_photo/{instance.name}.png")
    return (
        str(photo_path)
        if photo_path.exists()
        else "players_photo/default.png"
    )

class Player(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to=player_photo_path, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    age = models.IntegerField()
    skill = models.IntegerField()
    main_position = models.CharField(max_length=255)
    secondary_positions = models.CharField(max_length=255, null=True, blank=True)
    tertiary_positions = models.CharField(max_length=255, null=True, blank=True)
    GK = models.IntegerField(default=0)
    LB = models.IntegerField(default=0)
    CB = models.IntegerField(default=0)
    RB = models.IntegerField(default=0)
    WLB = models.IntegerField(default=0)
    WRB = models.IntegerField(default=0)
    LM = models.IntegerField(default=0)
    CDM = models.IntegerField(default=0)
    CM = models.IntegerField(default=0)
    CAM = models.IntegerField(default=0)
    RM = models.IntegerField(default=0)
    LW = models.IntegerField(default=0)
    RW = models.IntegerField(default=0)
    ST = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Update the photo field when saving the player instance
        self.photo = player_photo_path(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
