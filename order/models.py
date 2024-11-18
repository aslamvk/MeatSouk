from django.db import models
from django.contrib.auth.models import User
from address.models import Address
from products.models import Products
import uuid

# Create your models here.
class Order(models.Model):
    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('RazorPay', 'Razor Pay'),
        ('Wallet', 'Wallet')
    ]

    PAYMENT_STATUS = [
        ('Pending', 'Pending'),
        ('Success', 'Success'),
        ('Failure', 'Failure')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=100, unique=True, editable=False)
    total_price = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    payment_type = models.CharField(max_length=100, choices=PAYMENT_CHOICES)
    payment_status = models.CharField(max_length=100, choices=PAYMENT_STATUS,default='Pending')
    estimated_delivery = models.TimeField(blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    coupon_code = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = str(uuid.uuid4())  # Generate UUID as order number
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    STATUS = [
        ('Order Pending', 'Order Pending'),
        ('Order Confirmed', 'Order Confirmed'),
        ('Shipped', 'Shipped'),
        ('Out For Delivery', 'Out For Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
        ('Requested Return', 'Requested Return'),
        ('Approve Return', 'Approve Return'),
        ('Reject Return', 'Reject Return'),
    
    ]

    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=20, decimal_places=2)
    price = models.DecimalField(max_digits=100, decimal_places=2)
    status = models.CharField(max_length=100, choices=STATUS, default='Order Pending')
    subtotal_price = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    return_reason = models.TextField(blank=True, null=True)