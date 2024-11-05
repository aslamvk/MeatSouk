# Generated by Django 5.1.2 on 2024-11-01 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Success', 'Success'), ('Failure', 'Failure')], default='Pending', max_length=50),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_type',
            field=models.CharField(choices=[('COD', 'Cash on Delivery'), ('RazorPay', 'Razor Pay'), ('Wallet', 'Wallet')], max_length=50),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('order pending', 'order pending'), ('order confirmed', 'order confirmed'), ('shipped', 'shipped'), ('out for delivery', 'out for delivery'), ('delivered', 'delivered'), ('cancelled', 'cancelled'), ('requested return', 'requested return'), ('approve return', 'approve return'), ('reject return', 'reject return')], default='Order Pending', max_length=50),
        ),
    ]
