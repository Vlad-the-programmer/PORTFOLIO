from rest_framework import serializers
from .models import RecipeRequirement, Purchase, Ingredient, MenuItem


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'


class RecipeRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeRequirement
        fields = '__all__'


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'

