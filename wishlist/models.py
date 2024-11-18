from django.db import models
from django.contrib.auth.models import User
from products.models import Products

# Create your models here.
class Wishlist(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE)
    products = models.ForeignKey(Products,on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    