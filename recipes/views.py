from django.shortcuts import render
from django.db.models import Q
from .models import Recipe, Category

def home(request):
    # Get featured recipes for the carousel
    featured_recipes = Recipe.objects.filter(is_featured=True)[:5]
    
    # Get recommendations by categories
    categories = Category.objects.all()
    category_recipes = {}
    
    for category in categories:
        category_recipes[category] = Recipe.objects.filter(category=category)[:4]
    
    # Recent recipes
    recent_recipes = Recipe.objects.order_by('-created_at')[:8]
    
    context = {
        'featured_recipes': featured_recipes,
        'category_recipes': category_recipes,
        'recent_recipes': recent_recipes,
        'categories': categories,
    }
    
    return render(request, 'recipes/home.html', context)

def recipe_list(request):
    recipes = Recipe.objects.all()
    categories = Category.objects.all()
    
    # Filter by category if specified
    category_slug = request.GET.get('category')
    if category_slug:
        recipes = recipes.filter(category__slug=category_slug)
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        recipes = recipes.filter(
            Q(title__icontains=query) | 
            Q(ingredients__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    context = {
        'recipes': recipes,
        'categories': categories,
        'current_category': category_slug,
        'search_query': query,
    }
    
    return render(request, 'recipes/recipe_list.html', context)