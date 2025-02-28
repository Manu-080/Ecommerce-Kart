from django.urls import path

from .views import Home
from . import views

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('products/', views.products, name='products'),
    path('products/<slug:category_slug>', views.products, name='category_products'),

    path('product-detail/<slug:category_slug>/<slug:product_slug>', views.product_detail, name='product_detail'),

    path('search/', views.search, name='search'),

]
