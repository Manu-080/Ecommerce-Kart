from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, username, phone_number=None, password=None):
        if not email:
            raise ValueError("Email field should not be empty.")
        
        user = self.model(
            email = self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone_number=phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, first_name, last_name, username, phone_number=None, password=None):

        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=username,
            phone_number=phone_number,
            password=password,

        )
        user.is_staff=True
        user.is_superuser=True
        user.is_active=True

        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, unique=True, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager() # added custom manager

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username'] # not adding any extra fields.

    def __str__(self):
        return f"{self.first_name} {self.last_name}"