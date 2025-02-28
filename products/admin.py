from django.contrib import admin

from .models import Category, Product, ProductImage, ProductVariant

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    ordering = ['name']

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_available', 'created_date')
    ordering = ['-created_date']

class ProductVariantAdmin(admin.ModelAdmin):
    ordering = ['id']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(ProductVariant)
