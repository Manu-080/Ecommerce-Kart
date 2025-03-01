from django.db import models

from products.models import Product, ProductVariant
from users.models import User

# Create your models here.

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} Cart"
    

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product_variant = models.ManyToManyField(ProductVariant, related_name='cart_product_variants',)
    quantity = models.PositiveIntegerField(default=1)

    def sub_total(self):
        return self.product.discount_price*self.quantity

    def __str__(self):
        return f"{self.cart.user.username}--{self.product.name}"