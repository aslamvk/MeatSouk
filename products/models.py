from django.db import models
from category.models import Category
from pincode.models import Pincode

# Create your models here.
class Products(models.Model):
    UNIT_CHOICES = [
        ('kg', 'Kilogram'),
        ('piece', 'piece'),
    ]
    product_name = models.CharField(max_length=250)
    product_description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    product_unit = models.CharField(max_length=50, choices=UNIT_CHOICES, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    stock = models.DecimalField(max_digits=10, decimal_places=2)
    image1 = models.ImageField(upload_to='images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='images/', blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_listed = models.BooleanField(default=True)
    pincode = models.ManyToManyField(Pincode, related_name='products', blank=True)
