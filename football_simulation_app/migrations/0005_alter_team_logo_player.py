# Generated by Django 4.2.9 on 2024-01-08 22:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('football_simulation_app', '0004_remove_leagueteam_team_alter_country_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='')),
                ('age', models.IntegerField()),
                ('skill', models.IntegerField()),
                ('main_positions', models.CharField(max_length=255)),
                ('secondary_positions', models.CharField(blank=True, max_length=255, null=True)),
                ('tertiary_positions', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='football_simulation_app.country')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='football_simulation_app.team')),
            ],
        ),
    ]