# Generated by Django 5.1.2 on 2024-11-12 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0004_rename_usage_limit_coupon_coupon_limit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coupon',
            name='discount_amount',
        ),
    ]
