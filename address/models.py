from django.db import models
from django.contrib.auth.models import User
from pincode.models import Pincode

# Create your models here.

class Address(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='addresses')
    full_name = models.CharField(max_length=255,blank=True, null=True)
    phone_number = models.CharField(max_length=255)
    alternative_phone_number = models.CharField(max_length=255)
    pincode = models.ForeignKey(Pincode,on_delete=models.CASCADE,related_name='picodes')
    locality = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255)
    district = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    address = models.TextField()
    is_listed = models.BooleanField(default=True)
    ADDRESS_TYPE_CHOICES = [
        ('Home','Home'),
        ('Other','Other')
    ]
    address_type = models.CharField(max_length=12,choices=ADDRESS_TYPE_CHOICES)