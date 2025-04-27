from django.contrib import admin
from .models import Category, Recipe, UserPreference

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'cooking_time', 'difficulty', 'is_featured')
    list_filter = ('category', 'difficulty', 'is_featured')
    search_fields = ('title', 'ingredients')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user',)
    filter_horizontal = ('favorite_categories',)