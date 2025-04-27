from django.db import models

class Category(models.Model):
    id_category = models.CharField(max_length=10, unique=True, null=True, blank=True)  
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)  
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'

class Recipe(models.Model):
    DIFFICULTY_CHOICES = (
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='recipes')
    ingredients = models.TextField()
    instructions = models.TextField()
    cooking_time = models.PositiveIntegerField(help_text='Cooking time in minutes')
    serving_size = models.PositiveIntegerField(default=2)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)  
    id_meal = models.CharField(max_length=10, unique=True, null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_featured = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

class UserPreference(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    favorite_categories = models.ManyToManyField(Category, blank=True)
    disliked_ingredients = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s preferences"