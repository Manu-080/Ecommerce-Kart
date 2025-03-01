from django.db import models
from django.core.validators import RegexValidator

from users.models import User
# Create your models here.


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
        return f"{self.user.username} Address"