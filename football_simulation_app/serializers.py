# serializers.py
from rest_framework import serializers
from .models import Team

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'skill', 'defense_skill', 'midfield_skill', 'attack_skill', 'country', 'logo']
