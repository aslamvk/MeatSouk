# Generated by Django 5.1.2 on 2024-11-01 05:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0004_rename_phone_numnber_address_phone_number'),
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(editable=False, max_length=20, unique=True)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('payment_type', models.CharField(choices=[('COD', 'Cash on Delivery'), ('RazorPay', 'Razor Pay'), ('Wallet', 'Wallet')], max_length=20)),
                ('payment_status', models.CharField(choices=[('Pending', 'Pending'), ('Success', 'Success'), ('Failure', 'Failure')], default='Pending', max_length=20)),
                ('estimated_delivery', models.TimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='address.address')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.FloatField(default=0)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(choices=[('order pending', 'order pending'), ('order confirmed', 'order confirmed'), ('shipped', 'shipped'), ('out for delivery', 'out for delivery'), ('delivered', 'delivered'), ('cancelled', 'cancelled'), ('requested return', 'requested return'), ('approve return', 'approve return'), ('reject return', 'reject return')], default='Order Pending', max_length=20)),
                ('subtotal_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('return_reason', models.TextField(blank=True, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.products')),
            ],
        ),
    ]
