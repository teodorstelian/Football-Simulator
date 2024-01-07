from django import forms

class TeamSelectionForm(forms.Form):
    team_name = forms.CharField(label='Enter Team Name')