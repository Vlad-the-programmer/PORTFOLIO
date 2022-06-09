from django.shortcuts import render
from .models import RecipeRequirement, Purchase, Ingredient, MenuItem
from django.views.generic import ListView


# Create your views here.


def index(request):
    return render(request, 'home.html')


class MenuItemList(ListView):
    queryset = MenuItem.objects.all()
    context_object_name = 'menu_items_list'
    model = MenuItem
    template_name = "menuitem_list.html"


class IngredientsList(ListView):
    model = Ingredient
    template_name = "ingredients_list.html"
    queryset = Ingredient.objects.all()
    context_object_name = 'ingredients_list'


class RecipeRequirementList(ListView):
    model = RecipeRequirement
    template_name = "recipe_requirements.html"
    queryset = RecipeRequirement.objects.all()
    context_object_name = 'recipe_requirements'


class TotalRevenue(ListView):
    model = Ingredient
    template_name = 'revenue.html'
    queryset = Ingredient.objects.all()
    context_object_name = 'revenue'

    @property
    def get_revenue(self):
        revenue = 0
        revenue += float(Ingredient.objects.get('unit_price')) * float(Ingredient.objects.get('quantity'))



