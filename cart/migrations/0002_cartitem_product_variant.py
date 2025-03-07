# Generated by Django 5.1.6 on 2025-03-01 04:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
        ('products', '0005_delete_productvariationmanager'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='product_variant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cart_product_variants', to='products.productvariant'),
        ),
    ]
