from django.core.management.base import BaseCommand
from recipes.utils import fetch_categories_from_api

class Command(BaseCommand):
    help = 'Fetch categories from TheMealDB API'

    def handle(self, *args, **options):
        success = fetch_categories_from_api()
        if success:
            self.stdout.write(self.style.SUCCESS('Successfully fetched categories'))
        else:
            self.stdout.write(self.style.ERROR('Failed to fetch categories'))