from django.contrib import admin
from django.utils.text import slugify

from .models import Category, Product, ProductImage

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    ordering = ['name']

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_available', 'created_date')
    prepopulated_fields = {'slug':('name',)}
    ordering = ['-created_date']



admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
