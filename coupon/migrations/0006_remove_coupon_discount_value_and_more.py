# Generated by Django 5.1.2 on 2024-12-03 06:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0005_remove_coupon_discount_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='discount_value',
        ),
        migrations.AddField(
            model_name='coupon',
            name='discount_percentage',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(50)]),
        ),
    ]
