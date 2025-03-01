from django.db.models.signals import pre_save
from django.dispatch import receiver
from decimal import Decimal

from .models import Product

@receiver(pre_save, sender=Product)
def update_discount_price(sender, instance, **kwargs): # sender=Prduct , instace is the product object, and other keyword arguments.
    """Automatically calculate and update the discount price before saving."""
    if instance.discount is not None:
        instance.discount = int(((instance.price - instance.discount_price) / instance.price) * Decimal(100))
    