from django.db import models
from django.contrib.auth.models import User
from products.models import Products
# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    