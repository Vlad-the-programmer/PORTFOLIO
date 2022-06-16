from django.shortcuts import render, get_object_or_404, redirect
from .models import RecipeRequirement, Purchase, Ingredient, MenuItem
from django.views import generic
from rest_framework import viewsets
from rest_framework.decorators import api_view
from .serializers import IngredientSerializer, MenuItemSerializer, RecipeRequirementSerializer, PurchaseSerializer
from rest_framework.response import Response
from rest_framework import generics, mixins
from django.db.models import Sum, F
from .forms import IngredientForm, MenuItemForm, RecipeRequirementForm, PurchaseForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout


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


class MenuItemAPIList(generics.ListAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class RecipeRequirementAPIList(generics.ListAPIView):
    queryset = RecipeRequirement.objects.all()
    serializer_class = RecipeRequirementSerializer


class PurchasesAPIList(generics.ListAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer


class MenuItemAPIDetail(generics.RetrieveAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class MenuItemAPICreate(generics.CreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


class MenuAPIUpdate(generics.UpdateAPIView):
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()
    lookup_field = 'pk'


class MenuAPIDelete(generics.DestroyAPIView, generics.RetrieveAPIView):
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()
    lookup_field = 'pk'


class IngredientAPIList(generics.ListAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class IngredientAPICreate(generics.CreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class IngredientAPIDetail(generics.RetrieveAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    lookup_field = 'pk'


class IngredientAPIUpdate(generics.UpdateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    lookup_field = 'pk'


class IngredientAPIDelete(generics.RetrieveDestroyAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    lookup_field = 'pk'


class RecipeRequirementAPIList(generics.ListAPIView):
    queryset = RecipeRequirement.objects.all()
    serializer_class = RecipeRequirementSerializer


class RecipeRequirementAPICreate(generics.RetrieveAPIView):
    queryset = RecipeRequirement.objects.all()
    serializer_class = RecipeRequirementSerializer
    lookup_field = 'pk'


class RecipeRequirementAPIUpdate(generics.UpdateAPIView):
    queryset = RecipeRequirement.objects.all()
    serializer_class = RecipeRequirementSerializer
    lookup_field = 'pk'


class RecipeRequirementAPIDelete(generics.RetrieveDestroyAPIView):
    queryset = RecipeRequirement.objects.all()
    serializer_class = RecipeRequirementSerializer
    lookup_field = 'pk'


class RecipeRequirementsAPIDetail(generics.RetrieveAPIView):
    queryset = RecipeRequirement.objects.all()
    serializer_class = RecipeRequirementSerializer
    lookup_field = 'pk'


class PurchaseAPICreate(generics.CreateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer


class PurchaseAPIDetail(generics.RetrieveAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    lookup_field = 'pk'


class PurchaseAPIUpdate(generics.UpdateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    lookup_field = 'pk'


class PurchaseAPIDelete(generics.RetrieveDestroyAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    lookup_field = 'pk'


# class-based generic views


class MenuItemUpdate(generic.UpdateView):
    model = MenuItem
    queryset = MenuItem.objects.all()
    context_object_name = 'menuItem_update'


class PurchaseUpdate(generic.UpdateView):
    model = Purchase
    queryset = Purchase.objects.all()
    context_object_name = 'purchase_update'


class RecipeDelete(generic.DeleteView):
    queryset = RecipeRequirement.objects.all()
    model = RecipeRequirement


class IngredientDelete(generic.DeleteView):
    queryset = Ingredient.objects.all()
    model = Ingredient


class MenuItemDelete(generic.DeleteView):
    model = MenuItem
    queryset = MenuItem.objects.all()


class PurchaseDelete(generic.DeleteView):
    model = Purchase
    queryset = Purchase.objects.all()


class RecipeDetail(generic.DeleteView):
    queryset = RecipeRequirement.objects.all()
    # template_name = 'recipe_detail.html'
    context_object_name = 'recipe'


class IngredientDetail(generic.DetailView):
    queryset = Ingredient.objects.all()
    # template_name = 'ingredient_detail.html'
    context_object_name = 'ingredient'


class MenuItemDetail(generic.DetailView):
    queryset = MenuItem.objects.all()
    # template_name = 'menu_detail.html'
    context_object_name = 'menu_item'


class PurchaseDetail(generic.DetailView):
    queryset = Purchase.objects.all()
    context_object_name = 'purchase'
    # template_name = 'purchase_detail.html'

##
class HomeView(generic.TemplateView):
    template_name = "inventory/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredients"] = Ingredient.objects.all()
        context["menu_items"] = MenuItem.objects.all()
        context["purchases"] = Purchase.objects.all()
        return context


class IngredientList(generic.ListView):
    model = Ingredient
    template_name = 'inventory/ingredients_list.html'


class PurchasesList(generic.ListView):
    model = Purchase
    template_name = 'inventory/purchase_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objects'] = Purchase.objects.all()
        return context


class MenuList(generic.ListView):
    template_name = "inventory/menu_list.html"
    model = MenuItem


class RecipeCreate(generic.CreateView):
    model = RecipeRequirement
    template_name = 'inventory/add_recipe_requirement.html'
    form_class = RecipeRequirementForm


class IngredientCreate(generic.CreateView):
    model = Ingredient
    template_name = 'inventory/add_ingredient'
    form_class = IngredientForm


class MenusItemCreate(generic.CreateView):
    model = MenuItem
    template_name = 'inventory/add_menu_item.html'
    form_class = MenuItemForm

#
# class PurchaseCreate(generic.CreateView):
#     model = Purchase
#     template_name = 'inventory/add_purchase.html'
#     form_class = PurchaseForm


class IngredientUpdate(generic.UpdateView):
    model = Ingredient
    template_name = 'inventory/update_ingredient.html'
    form_class = IngredientForm


class NewPurchaseView(generic.TemplateView):
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


class ReportView(generic.TemplateView):
    template_name = "inventory/reports.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["purchases"] = Purchase.objects.all()
        revenue = Purchase.objects.aggregate(
            revenue=Sum("menu_item__price"))["revenue"]
        total_cost = 0
        for purchase in Purchase.objects.all():
            for recipe_requirement in purchase.menu_item.reciperequirement_set.all():
                total_cost += recipe_requirement.ingredient.price_per_unit * \
                    recipe_requirement.quantity

        context["revenue"] = revenue
        context["total_cost"] = total_cost
        context["profit"] = revenue - total_cost


def log_out(request):
    logout(request)
    return redirect("/")



