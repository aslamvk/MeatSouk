# Generated by Django 5.1.2 on 2024-11-27 05:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_rename_discount_amount_order_coupon_discount_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(max_length=20, unique=True)),
                ('invoice_date', models.DateTimeField(auto_now_add=True)),
                ('order_item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='invoice', to='order.orderitem')),
            ],
        ),
    ]
