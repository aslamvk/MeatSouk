from django.db import models
from products.models import Products
from category.models import Category

# Create your models here.
class Product_Offers(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    offer_discount = models.DecimalField(max_digits=10, decimal_places=2)
    offer_name = models.CharField(null=True,blank=True)
    offer_details = models.TextField(null=True,blank=True)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Category_Offers(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    offer_discount = models.DecimalField(max_digits=10, decimal_places=2)
    offer_name = models.CharField(null=True,blank=True)
    offer_details = models.TextField(null=True,blank=True)
    valid_from = models.DateTimeField(null=True, blank=True)
    valid_to = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)