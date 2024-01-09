from django import forms

class TeamSelectionForm(forms.Form):
    team_name = forms.CharField(label='Enter Team Name')

class SelectPlayerForm(forms.Form):
    player_name = forms.CharField(label='Player Name', max_length=100)