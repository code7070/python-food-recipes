# recipes/utils.py
import requests
from django.utils.text import slugify
from .models import Category, Recipe

def fetch_categories_from_api():
    """Fetch categories from TheMealDB API and save to database"""
    url = "https://www.themealdb.com/api/json/v1/1/categories.php"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        for category_data in data['categories']:
            # Check if category already exists
            category, created = Category.objects.update_or_create(
                id_category=category_data['idCategory'],
                defaults={
                    'name': category_data['strCategory'],
                    'slug': slugify(category_data['strCategory']),
                    'description': category_data['strCategoryDescription'],
                    'image_url': category_data['strCategoryThumb']
                }
            )
        return True
    return False

def fetch_recipes_by_category(category_name):
    """
    Fetch recipes for a specific category from TheMealDB API
    
    Args:
        category_name (str): The name of the category to fetch recipes for
        
    Returns:
        bool: True if successful, False otherwise
    """
    url = f"https://www.themealdb.com/api/json/v1/1/filter.php?c={category_name}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Check if meals exist in the response
        if 'meals' in data and data['meals']:
            # Get the category object
            try:
                category = Category.objects.get(name=category_name)
            except Category.DoesNotExist:
                print(f"Category '{category_name}' not found in database")
                return False
            
            # Process each meal
            for meal_data in data['meals']:
                # Check if recipe already exists
                recipe, created = Recipe.objects.update_or_create(
                    id_meal=meal_data['idMeal'],
                    defaults={
                        'title': meal_data['strMeal'],
                        'slug': slugify(meal_data['strMeal']),
                        'category': category,
                        'image_url': meal_data['strMealThumb'],
                        # Provide default values for required fields
                        'ingredients': 'Fetching ingredients...',
                        'instructions': 'Fetching instructions...',
                        'cooking_time': 30,  # Default value
                        'serving_size': 4,  # Default value
                    }
                )
                
                # If this is a new recipe, we'll need to fetch the full details
                if created:
                    fetch_recipe_details(meal_data['idMeal'])
                    
            return True
        else:
            print(f"No meals found for category '{category_name}'")
            return False
    return False

def fetch_recipe_details(meal_id):
    """
    Fetch detailed information for a specific recipe from TheMealDB API
    
    Args:
        meal_id (str): The ID of the meal to fetch details for
        
    Returns:
        bool: True if successful, False otherwise
    """
    url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        if 'meals' in data and data['meals']:
            meal_data = data['meals'][0]
            
            # Get the recipe
            try:
                recipe = Recipe.objects.get(id_meal=meal_id)
            except Recipe.DoesNotExist:
                print(f"Recipe with ID '{meal_id}' not found in database")
                return False
            
            # Extract ingredients and measurements
            ingredients = []
            for i in range(1, 21):  # TheMealDB has up to 20 ingredients
                ingredient_key = f'strIngredient{i}'
                measure_key = f'strMeasure{i}'
                
                if ingredient_key in meal_data and meal_data[ingredient_key]:
                    ingredient = meal_data[ingredient_key]
                    measure = meal_data.get(measure_key, '')
                    ingredients.append(f"{measure} {ingredient}".strip())
            
            # Update recipe with detailed information
            recipe.ingredients = "\n".join(ingredients)
            recipe.instructions = meal_data.get('strInstructions', '')
            recipe.cooking_time = 30  # Default value, as TheMealDB doesn't provide this
            recipe.serving_size = 4  # Default value
            recipe.save()
            
            return True
        else:
            print(f"No details found for meal ID '{meal_id}'")
            return False
    return False
