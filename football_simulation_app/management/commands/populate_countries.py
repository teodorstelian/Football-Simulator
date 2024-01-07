from django.core.management.base import BaseCommand
from football_simulation_app.models import Country
from src.initial_data import COUNTRIES

class Command(BaseCommand):
    help = 'Populate initial countries data'

    def handle(self, *args, **options):
        for country_name, europe_data in COUNTRIES.items():
            country, created = Country.objects.get_or_create(
                name=country_name,
                defaults={
                    "ucl_places": europe_data["ucl"],
                    "uel_places": europe_data["uel"],
                    "uecl_places": europe_data["uecl"],
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created country: {country.name}'))
            else:
                self.stdout.write(self.style.SUCCESS(f'Country already exists: {country.name}'))
