from django.core.management.base import BaseCommand
from recipes.utils import fetch_recipes_by_category
from recipes.models import Category

class Command(BaseCommand):
    help = 'Fetch recipes from TheMealDB API for specified categories'

    def add_arguments(self, parser):
        parser.add_argument(
            '--categories',
            nargs='+',
            type=str,
            help='List of category names to fetch recipes for. If not provided, all categories will be used.',
        )

    def handle(self, *args, **options):
        categories = options['categories']
        
        if not categories:
            # If no categories specified, use all categories from the database
            categories = Category.objects.values_list('name', flat=True)
            self.stdout.write(f"No categories specified. Will fetch recipes for all {len(categories)} categories.")
        
        success_count = 0
        for category_name in categories:
            self.stdout.write(f"Fetching recipes for category: {category_name}")
            if fetch_recipes_by_category(category_name):
                success_count += 1
                self.stdout.write(self.style.SUCCESS(f"Successfully fetched recipes for category: {category_name}"))
            else:
                self.stdout.write(self.style.ERROR(f"Failed to fetch recipes for category: {category_name}"))
        
        self.stdout.write(self.style.SUCCESS(f"Completed fetching recipes. Successfully processed {success_count} out of {len(categories)} categories."))
