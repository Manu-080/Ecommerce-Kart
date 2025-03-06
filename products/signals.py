from django.db.models.signals import pre_save
from django.dispatch import receiver
from decimal import Decimal

from .models import Product

@receiver(pre_save, sender=Product)
def update_discount_price(sender, instance, **kwargs): # sender=Prduct , instace is the product object, and other keyword arguments.
    """Automatically calculate and update the discount price before saving."""
    if instance.discount is None and instance.price and instance.discount_price:
        # Convert float to Decimal before performing arithmetic
        price = Decimal(str(instance.price)) # price = Decimal('29,999.00')
        discount_price = Decimal(str(instance.discount_price)) # discount_price = Decimal('20,999.00')

        instance.discount = int(((price - discount_price) / price) * 100)
    