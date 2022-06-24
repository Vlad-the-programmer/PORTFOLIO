from django.shortcuts import render, get_object_or_404, redirect
from .models import RecipeRequirement, Purchase, Ingredient, MenuItem
from django.views import generic
from rest_framework import viewsets
from rest_framework.decorators import api_view
from .serializers import IngredientSerializer, MenuItemSerializer, RecipeRequirementSerializer, PurchaseSerializer
from rest_framework.response import Response
from rest_framework import generics, mixins
from django.db.models import Sum
from .forms import IngredientForm, MenuItemForm, RecipeRequirementForm, PurchaseForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
# Create your views here.
# @api_view(['GET'])
# def ingredients_list(request):
#     ingredients = Ingredient.objects.all()
#     serializer = IngredientSerializer(ingredients, many=True)
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# def menu_item_list(request):
#     menu_items = MenuItem.objects.all()
#     serializer = MenuItemSerializer(menu_items, many=True)
#     return Response(serializer.data)
#
#
# @api_view(['GET'])
# def menu_item_detail(request, pk):
#     menu_item = MenuItem.objects.get(id=pk)
#     serializer = MenuItemSerializer(menu_item, many=False)
#     return Response(serializer.data)


# @api_view(['POST'])
# # def menu_create(request):
# #     serializer = MenuItemSerializer(data=request.data)
# #     if serializer.is_valid():
# #         serializer.save()
# #     return Response(serializer.data)


# @api_view(['POST'])
# def menu_update(request, pk):
#     menu_item = MenuItem.objects.get(id=pk)
#     serializer = MenuItemSerializer(instance=menu_item, data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#     return Response(serializer.data)


# class MenuItemAPIList(generics.ListAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer
#
#
# class RecipeRequirementAPIList(generics.ListAPIView):
#     queryset = RecipeRequirement.objects.all()
#     serializer_class = RecipeRequirementSerializer
#
#
# class PurchasesAPIList(generics.ListAPIView):
#     queryset = Purchase.objects.all()
#     serializer_class = PurchaseSerializer
#
#
# class MenuItemAPIDetail(generics.RetrieveAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer
#
#
# class MenuItemAPICreate(generics.CreateAPIView):
#     queryset = MenuItem.objects.all()
#     serializer_class = MenuItemSerializer
#
#
# class MenuAPIUpdate(generics.UpdateAPIView):
#     serializer_class = MenuItemSerializer
#     queryset = MenuItem.objects.all()
#     lookup_field = 'pk'
#
#
# class MenuAPIDelete(generics.DestroyAPIView, generics.RetrieveAPIView):
#     serializer_class = MenuItemSerializer
#     queryset = MenuItem.objects.all()
#     lookup_field = 'pk'
#
#
# class IngredientAPIList(generics.ListAPIView):
#     queryset = Ingredient.objects.all()
#     serializer_class = IngredientSerializer
#
#
# class IngredientAPICreate(generics.CreateAPIView):
#     queryset = Ingredient.objects.all()
#     serializer_class = IngredientSerializer
#
#
# class IngredientAPIDetail(generics.RetrieveAPIView):
#     queryset = Ingredient.objects.all()
#     serializer_class = IngredientSerializer
#     lookup_field = 'pk'
#
#
# class IngredientAPIUpdate(generics.UpdateAPIView):
#     queryset = Ingredient.objects.all()
#     serializer_class = IngredientSerializer
#     lookup_field = 'pk'
#
#
# class IngredientAPIDelete(generics.RetrieveDestroyAPIView):
#     queryset = Ingredient.objects.all()
#     serializer_class = IngredientSerializer
#     lookup_field = 'pk'
#
#
# class RecipeRequirementAPIList(generics.ListAPIView):
#     queryset = RecipeRequirement.objects.all()
#     serializer_class = RecipeRequirementSerializer
#
#
# class RecipeRequirementAPICreate(generics.RetrieveAPIView):
#     queryset = RecipeRequirement.objects.all()
#     serializer_class = RecipeRequirementSerializer
#     lookup_field = 'pk'
#
#
# class RecipeRequirementAPIUpdate(generics.UpdateAPIView):
#     queryset = RecipeRequirement.objects.all()
#     serializer_class = RecipeRequirementSerializer
#     lookup_field = 'pk'
#
#
# class RecipeRequirementAPIDelete(generics.RetrieveDestroyAPIView):
#     queryset = RecipeRequirement.objects.all()
#     serializer_class = RecipeRequirementSerializer
#     lookup_field = 'pk'
#
#
# class RecipeRequirementsAPIDetail(generics.RetrieveAPIView):
#     queryset = RecipeRequirement.objects.all()
#     serializer_class = RecipeRequirementSerializer
#     lookup_field = 'pk'
#
#
# class PurchaseAPICreate(generics.CreateAPIView):
#     queryset = Purchase.objects.all()
#     serializer_class = PurchaseSerializer
#
#
# class PurchaseAPIDetail(generics.RetrieveAPIView):
#     queryset = Purchase.objects.all()
#     serializer_class = PurchaseSerializer
#     lookup_field = 'pk'
#
#
# class PurchaseAPIUpdate(generics.UpdateAPIView):
#     queryset = Purchase.objects.all()
#     serializer_class = PurchaseSerializer
#     lookup_field = 'pk'
#
#
# class PurchaseAPIDelete(generics.RetrieveDestroyAPIView):
#     queryset = Purchase.objects.all()
#     serializer_class = PurchaseSerializer
#     lookup_field = 'pk'
#

# class-based generic views


class MenuItemUpdate(LoginRequiredMixin, UpdateView):
    model = MenuItem
    queryset = MenuItem.objects.all()
    context_object_name = 'menuItem_update'


class PurchaseUpdate(LoginRequiredMixin, UpdateView):
    model = Purchase
    queryset = Purchase.objects.all()
    context_object_name = 'purchase_update'


class RecipeDelete(LoginRequiredMixin, generic.edit.DeleteView):
    queryset = RecipeRequirement.objects.all()
    model = RecipeRequirement
    context_object_name = 'recipe'
    success_url = reverse_lazy('inventory:menu')

    def get_object(self):
        pk_ = self.kwargs.get('pk')
        return get_object_or_404(RecipeRequirement, pk=pk_)


class IngredientDelete(LoginRequiredMixin, generic.edit.DeleteView):
    queryset = Ingredient.objects.all()
    model = Ingredient
    context_object_name = 'ingredient'
    success_url = reverse_lazy('inventory:ingredients')

    def get_object(self):
        pk_ = self.kwargs.get('pk')
        return get_object_or_404(Ingredient, pk=pk_)


class MenuItemDelete(LoginRequiredMixin, generic.edit.DeleteView):
    model = MenuItem
    queryset = MenuItem.objects.all()
    context_object_name = 'menu'
    success_url = reverse_lazy('inventory:menu')

    def get_object(self):
        pk_ = self.kwargs.get('pk')
        return get_object_or_404(MenuItem, pk=pk_)


class PurchaseDelete(LoginRequiredMixin, generic.edit.DeleteView):
    model = Purchase
    queryset = Purchase.objects.all()
    context_object_name = 'purchase'
    success_url = reverse_lazy('inventory:purchases')

    def get_object(self):
        pk_ = self.kwargs.get('pk')
        return get_object_or_404(Purchase, pk=pk_)


class HomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = "inventory/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredients"] = Ingredient.objects.all()
        context["menu_items"] = MenuItem.objects.all()
        context["purchases"] = Purchase.objects.all()
        return context


class IngredientList(LoginRequiredMixin, generic.ListView):
    model = Ingredient
    template_name = 'inventory/ingredients_list.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objects'] = Ingredient.objects.all()
        return context


class PurchasesList(LoginRequiredMixin, generic.ListView):
    model = Purchase
    template_name = 'inventory/purchase_list.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objects'] = Purchase.objects.all()
        return context


class MenuList(LoginRequiredMixin, generic.ListView):
    template_name = "inventory/menu_list.html"
    model = MenuItem
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objects'] = MenuItem.objects.all()
        return context


class RecipeCreate(LoginRequiredMixin, CreateView):
    model = RecipeRequirement
    template_name = 'inventory/add_recipe_requirement.html'
    form_class = RecipeRequirementForm


class IngredientCreate(LoginRequiredMixin, CreateView):
    model = Ingredient
    template_name = 'inventory/add_ingredient.html'
    form_class = IngredientForm


class MenusItemCreate(LoginRequiredMixin, CreateView):
    model = MenuItem
    template_name = 'inventory/add_menu_item.html'
    form_class = MenuItemForm


class IngredientUpdate(LoginRequiredMixin, UpdateView):
    model = Ingredient
    template_name = 'inventory/ingredient_update.html'
    form_class = IngredientForm
    success_url = 'ingredients/'


class NewPurchaseView(LoginRequiredMixin, generic.TemplateView):
    template_name = "inventory/add_purchase.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu_items"] = [X for X in MenuItem.objects.all() if X.available()]
        return context

    def post(self, request):
        menu_item_id = request.POST["menu_item"]
        menu_item = MenuItem.objects.get(pk=menu_item_id)
        requirements = menu_item.reciperequirement_set
        purchase = Purchase(menu_item=menu_item)

        for requirement in requirements.all():
            required_ingredient = requirement.ingredient
            required_ingredient.quantity -= requirement.quantity
            required_ingredient.save()

        purchase.save()
        return redirect("/purchases")


# Does not work
class ReportView(LoginRequiredMixin, generic.TemplateView):
    template_name = "inventory/reports.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["purchases"] = Purchase.objects.all()
        revenue = Purchase.objects.aggregate(
            revenue=Sum("menu_item__price"))["revenue"]
        total_cost = 0
        for purchase in Purchase.objects.all():
            for recipe_requirement in purchase.menu_item.reciperequirement_set.all():
                total_cost += float(recipe_requirement.ingredient.price_per_unit) * \
                    float(recipe_requirement.quantity)

        context["revenue"] = revenue
        context["total_cost"] = total_cost
        context["profit"] = float(revenue) - float(total_cost)
        return context


def log_out(request):
    logout(request)
    return redirect("/")



