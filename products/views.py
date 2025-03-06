from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator

from .models import Product, Category
from cart.models import CartItem

# Create your views here.

# HOME PAGE 
class Home(ListView):
    model = Product
    template_name = "product/home.html"
    context_object_name = "products"  # Context name to access products in frontend.
    paginate_by = 8


# function based view for home page.
# def home(request):
#     products = Product.objects.all()[:10]
#     context = {
#         'products':products
#     }
#     return render(request, 'product/home.html', context)


# ALL PRODUCTS
def products(request, category_slug=None):

    if category_slug != None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)
    else:
        products = Product.objects.all()

    products_count = products.count()
    all_categories = Category.objects.all()

    paginator = Paginator(products, 6) # show 6 products.
    page_number = request.GET.get('page') # get the page number from the url
    products = paginator.get_page(page_number) # get the products for the page number

    context = {
        'products':products,
        'products_count':products_count,
        'all_categories':all_categories,
    }
    return render(request, 'product/products.html', context)


# SEARCH FUNCTION BASIC ELASTIC SEARCH WONT WORK IN WINDOWS EITHER USE LINUX OR USE DOCKER CONTAINERISATION.
#  i will implement elastic search with fuzziness later at end of this project also i need to implement redis cache.
def search(request):
    if request.method == 'GET':
        serach_item = request.GET.get('keyword')
        if not serach_item or len(serach_item) > 30:
            serach_item = Product.objects.none()
            return redirect('page_404')
            # i should implement 404 page later
        else:
            serach_output = Product.objects.filter(name__icontains = serach_item)
    if serach_output:
        product_count = serach_output.count()
    else:
        product_count = 0

    
    
    context = {
        'products':serach_output,
        'products_count':product_count,
    }

    return render(request, 'product/products.html', context)

# PRODUCT DETAILS

def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)

    if request.user.is_authenticated:
        incart = CartItem.objects.filter(cart__user=request.user, product=product)
    else:
        incart = None

    product_reviews = product.reviews.all()
        
    context = {
        'product':product,
        'in_cart':incart,
        'product_reviews':product_reviews,
        
    }
    return render(request, 'product/product_detail.html', context)




# 404 PAGE 
def page_404(request):
    return render(request, 'basic_include/404_page.html')