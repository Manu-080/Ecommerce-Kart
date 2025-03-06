from django.contrib import admin
import admin_thumbnails

from .models import Category, Product, ProductImage, ProductVariant, Review

# Register your models here.

@admin_thumbnails.thumbnail('image') # this decorator is used to show images in admin panel it is intalled as a package.
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    ordering = ['name']


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'is_available', 'created_date')
    ordering = ['-created_date']
    inlines = [ProductImageInline]


class ProductVariantAdmin(admin.ModelAdmin):
    ordering = ['id']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(ProductVariant)
admin.site.register(Review)
