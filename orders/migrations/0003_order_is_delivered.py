# Generated by Django 5.1.6 on 2025-03-04 06:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_orderitem_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='is_delivered',
            field=models.BooleanField(default=False),
        ),
    ]
