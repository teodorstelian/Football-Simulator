# Generated by Django 4.2.9 on 2024-01-09 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('football_simulation_app', '0006_player_cam_player_cb_player_cdm_player_cm_player_gk_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='attack_skill',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='team',
            name='defense_skill',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='team',
            name='midfield_skill',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='team',
            name='skill',
            field=models.IntegerField(default=0),
        ),
    ]