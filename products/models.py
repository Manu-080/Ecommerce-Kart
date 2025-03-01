from django.db import models
from django.utils.text import slugify
from django.urls import reverse
import uuid

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

 
    def save(self, *args, **kwargs):
        if not self.slug: # Only generate slug if it doesn't exist
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Category.objects.filter(slug=slug).exists(): # To eliminate duplicate slug name.
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    def get_url(self):
        return reverse('category_products', args=[self.slug]) # category_products is the name of the URL pattern in urls.py
    


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200,unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.PositiveIntegerField(default=0)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='uploads/product')
    stock = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    priority = models.PositiveBigIntegerField(blank=True, null=True)
    discount = models.PositiveIntegerField(blank=True, null=True) # percentage 
    discount_price = models.PositiveIntegerField(default=0, null=True, blank=True) # last price

    

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name
    
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug]) # product_detail is the name of the URL pattern in urls.py
    

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='uploads/product/product_images')


    def __str__(self):
        return self.product.name
    
# PRODUCT VARIATION SECTION.    

class ProductVariationManager(models.Manager):
    def colors(self):
        return self.filter(variant_type = 'color')
    
    def sizes(self):
        return self.filter(variant_type = 'size')
    
    def variants(self):
        return self.filter(variant_type = 'variant')


variation_choice = (
    ('color','color'),
    ('size','size'),
    ('variant', 'variant')
)

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    variant_type = models.CharField(max_length=100, choices=variation_choice)
    variant_value = models.CharField(max_length=100)
    sku =models.CharField(max_length=100, unique=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    stock = models.PositiveIntegerField(default=0)


    objects = ProductVariationManager()

    def save(self, *args, **kwargs):
        if not self.sku:
            # Generate SKU using product name + random ID
            base_sku = self.product.name.upper().replace(" ", "-")
            unique_id = str(uuid.uuid4())[:8]  # Short unique identifier
            self.sku = f"{base_sku}-{unique_id}"
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.product.name}  | {self.variant_value}"
    