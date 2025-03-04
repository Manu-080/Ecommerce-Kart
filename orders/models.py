from django.db import models
from django.core.validators import RegexValidator
from decimal import Decimal

from users.models import User
from products.models import Product
# Create your models here.


# TO SAVE USER ADDRESS
class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_addresses')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(
        max_length=15, 
        validators=[RegexValidator(regex=r'^\d{10,15}$', message="Enter a valid phone number")] 
    )  # Only allows digits, length 10-15                REGEX -> defines the allowed pattern MESSAGE -> Error message if validation fails
    address = models.CharField(max_length=200)
    landmark = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} Address ID: {self.id}"


# ORDER MODEL FOR MAKING ORDER AT EVRYTIME
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending','Pending'),
        ('processing','Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(UserAddress, on_delete=models.SET_NULL, null=True) # If user deleted one of his adress then that model object should not be deleted.
    total_price = models.DecimalField(max_digits=16, decimal_places=2,default=Decimal('0.00'))
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if self.status == 'delivered': # would only True if order is delivered.
            self.is_delivered = True
        else:
            self.is_delivered = False # Ensure consistency when status changes
        return super().save(*args, **kwargs)


    def __str__(self):
        return f"Order: {self.id} | Name: {self.user.username}"
    


# ORDER ITEMS , PRODUCTS THE USER BUYING AT EVERY ORDER EG: A ORDER WOULD HAVE MULTIPLE ORDER ITEMS.
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_order_items', null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.quantity * self.price
    
    def __str__(self):
        return f"Quantity: {self.quantity} | Product: {self.product.name} | User:-> {self.order.user.username}"
    
    

# ORDER PAYMENT MODEL
class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payments')
    payment_method = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=16, decimal_places=2)
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Payment {self.transaction_id} | {self.amount} | {self.created_at}"
    