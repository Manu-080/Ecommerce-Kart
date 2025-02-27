from django.shortcuts import render
from django.views.generic import ListView

from .models import Product

# Create your views here.

class Home(ListView):
    model = Product
    template_name = "product/home.html"
    context_object_name = "products"  # ontext name to access products in frontend.
    paginate_by = 8


# function based view for home page.
# def home(request):
#     products = Product.objects.all()[:10]
#     context = {
#         'products':products
#     }
#     return render(request, 'product/home.html', context)


def products(request):
    pass

def search(request):
    pass

def product_detail(request):
    pass