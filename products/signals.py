from django.db.models.signals import pre_save
from django.dispatch import receiver
from decimal import Decimal

from .models import Product

@receiver(pre_save, sender=Product)
def update_discount_price(sender, instance, **kwargs): # sender=Prduct , instace is the product object, and other keyword arguments.
    """Automatically calculate and update the discount price before saving."""
    instance.discount_price = int(instance.price * (Decimal(1) - instance.discount/Decimal(100)))
    