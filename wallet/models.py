from django.db import models
from  django.contrib.auth.models import User

# Create your models here.


class Wallet(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    created_at = models.DateField(auto_now_add=True)

class WalletTransaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('Refund', 'Refund'),
        ('Cancellation', 'Cancellation'),
        ('Debited', 'Debited'),
    ]
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=100,choices=TRANSACTION_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    created_at = models.DateField(auto_now_add=True)


