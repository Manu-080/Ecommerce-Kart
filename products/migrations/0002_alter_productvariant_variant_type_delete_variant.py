# Generated by Django 5.1.6 on 2025-02-28 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productvariant',
            name='variant_type',
            field=models.CharField(choices=[('color', 'color'), ('size', 'size'), ('variant', 'variant')], max_length=100),
        ),
        migrations.DeleteModel(
            name='Variant',
        ),
    ]
