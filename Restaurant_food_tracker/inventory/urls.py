from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'inventory'
urlpatterns = [

    # path('', views.HomeView.as_view(), name='home'),
    # path('menuItems/', views.MenuItemAPIList.as_view(), name='menu-items'),
    # path('recipe_requirements/', views.RecipeRequirementAPIList.as_view(), name='recipe-requirements'),
    # path('report/', views.ReportView.as_view(), name='reports'),
    # path('newpurchase/', views.NewPurchaseView.as_view(), name='new_purchase'),

    # path('menu-list/', views.MenuItemAPIList.as_view(), name='menu-items'),
    # path('menu-create/', views.MenuItemAPICreate.as_view(), name='menu-create'),
    # path('menu-detail/<int:pk>/', views.MenuItemAPIDetail.as_view(), name='menu-detail'),
    # path('menu-update/<int:pk>/', views.MenuAPIUpdate.as_view(), name='menu-update'),
    # path('menu-delete/<int:pk>/', views.MenuAPIDelete.as_view(), name='menu-delete'),
    # path('ingredient-detail/<int:pk>/', views.IngredientAPIDetail.as_view(), name='ingredients-detail'),
    # path('ingredient-update/<int:pk>/', views.IngredientAPIUpdate.as_view(), name='ingredients-update'),
    # path('ingredient-delete/<int:pk>/', views.IngredientAPIDelete.as_view(), name='ingredients-delete'),
    # path('ingredient-create', views.IngredientAPICreate.as_view(), name='ingredient-create'),
    #
    # path('recipe-requirements/', views.RecipeRequirementAPIList.as_view(), name='recipe-list'),
    # path('recipe-detail/<int:pk>/', views.RecipeRequirementsAPIDetail.as_view(), name='recipe-detail'),
    # path('recipe-update/<int:pk>/', views.IngredientAPIUpdate.as_view(), name='recipe-update'),
    # path('recipe-delete/<int:pk>/', views.IngredientAPIDelete.as_view(), name='recipe-delete'),
    # path('recipe-create/', views.IngredientAPICreate.as_view(), name='recipe-create'),
    #
    # path('purchases/', views.PurchasesAPIList.as_view(), name='purchases-list'),
    # path('purchase-detail/<int:pk>/', views.PurchaseAPIDetail.as_view(), name='purchases-detail'),
    # path('purchase-update/<int:pk>/', views.PurchaseAPIUpdate.as_view(), name='purchases-update'),
    # path('purchase-delete/<int:pk>/', views.PurchaseAPIDelete.as_view(), name='purchases-delete'),
    # path('purchase-create/', views.PurchaseAPICreate.as_view(), name='purchases-create'),

    path("logout/", views.log_out, name="logout"),
    path('accounts/login/', auth_views.LoginView.as_view(), name="login"),
    path('', views.HomeView.as_view(), name='home'),
    path('ingredients/', views.IngredientList.as_view(), name="ingredients"),
    path('ingredients/new', views.IngredientCreate.as_view(), name="add_ingredient"),
    path('ingredients/<slug:pk>/update', views.IngredientUpdate.as_view(), name="update_ingredient"),
    path('menu/', views.MenuList.as_view(), name="menu"),
    path('menu/new', views.MenusItemCreate.as_view(), name="add_menu_item"),
    path('reciperequirement/new', views.RecipeCreate.as_view(), name="add_recipe_requirement"),
    path('purchases/', views.PurchasesList.as_view(), name="purchases"),
    path('purchases/new', views.NewPurchaseView.as_view(), name="add_purchase"),
    path('reports/', views.ReportView.as_view(), name="reports"),
    path('ingredient/<slug:pk>/delete/', views.IngredientDelete.as_view(), name="delete_ingredient"),
    path('reciperequirement/<slug:pk>/delete/', views.RecipeDelete.as_view(), name="delete_recipe_requirement"),
    path('menu/<slug:pk>/delete/', views.MenuItemDelete.as_view(), name="delete_menu"),
    path('purchase/<slug:pk>/delete/', views.PurchaseDelete.as_view(), name="delete_purchase"),

]