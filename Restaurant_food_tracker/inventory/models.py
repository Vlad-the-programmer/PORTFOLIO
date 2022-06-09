import datetime

from django.db import models


class Ingredient(models.Model):

    name = models.CharField(max_length=20, blank=True)
    quantity = models.IntegerField(null=False, verbose_name='Quantity')
    unit = models.CharField(max_length=20, blank=True)
    unit_price = models.FloatField(null=False, verbose_name='Price per unit')

    def get_absolute_url(self):
        return 'ingredient'

    def __str__(self):
        return f'{self.name} {self.quantity} {self.unit_price}'

    def get_revenue(self):
        revenue += float(self.unit_price * self.quantity)


class MenuItem(models.Model):
    title = models.CharField(max_length=20, null=False)
    price = models.FloatField(null=False)

    def __str__(self):
        return f'{self.title} {self.price}'


class RecipeRequirement(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(verbose_name='Quantity', null=False)

    def __str__(self):
        return f'{self.menu_item} {self.ingredient} {self.quantity}'


class Purchase(models.Model):
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(datetime.datetime.now(), editable=False)





