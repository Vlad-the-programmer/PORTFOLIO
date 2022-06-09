from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name='home'),
    path('menuItems/', views.MenuItemList.as_view(), name='menu_items'),
    path('ingredients/', views.IngredientsList.as_view(), name='ingredients_list'),
    path('recipe_requirements/', views.RecipeRequirementList.as_view(), name='recipe_requirements'),
    path('revenue/', views.TotalRevenue.as_view(), name='revenue'),

]
