from django.contrib import admin
from .models import RecipeRequirement, Purchase, Ingredient, MenuItem
# Register your models here.
admin.site.register(RecipeRequirement)
admin.site.register(Purchase)
admin.site.register(Ingredient)
admin.site.register(MenuItem)