# Generated by Django 5.1.6 on 2025-02-28 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_productvariationmanager'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductVariationManager',
        ),
    ]
