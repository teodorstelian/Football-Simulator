from django import forms

class TeamSelectionForm(forms.Form):
    team_name = forms.CharField(label='Enter Team Name')

class SelectPlayerForm(forms.Form):
    player_name = forms.CharField(label='Player Name', max_length=100)

class LineupForm(forms.Form):
    country = forms.CharField()
    team = forms.CharField()
    GK = forms.CharField()
    LB = forms.CharField()
    CB1 = forms.CharField()
    CB2 = forms.CharField()
    RB = forms.CharField()
    CDM1 = forms.CharField()
    CDM2 = forms.CharField()
    CAM = forms.CharField()
    LW = forms.CharField()
    RW = forms.CharField()
    ST = forms.CharField()