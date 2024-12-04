from django.db import models
from products.models import Products
from category.models import Category
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Product_Offers(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    offer_percentage = models.DecimalField(max_digits=10, decimal_places=2,validators=[MinValueValidator(0), MaxValueValidator(80)],null=True)
    offer_name = models.CharField(null=True,blank=True)
    offer_details = models.TextField(null=True,blank=True)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Category_Offers(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    offer_percentage = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(80)], null=True)
    offer_name = models.CharField(null=True,blank=True)
    offer_details = models.TextField(null=True,blank=True)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)