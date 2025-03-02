from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Cart, CartItem
from products.models import Product, ProductVariant
from orders.models import UserAddress
# Create your views here.

def cart(request):
    total_price = 0
    discount = 0
    tax = 0
    total = 0
    discount_price = 0

    current_user = request.user

    if current_user.is_authenticated:
        cart_items = CartItem.objects.filter(cart__user = current_user)
    else:
        cart_items = CartItem.objects.none()

    for items in cart_items:
        if items.product.stock <= 0:
            continue
        total_price += (items.product.price * items.quantity)
        discount += (items.product.price - items.product.discount_price)
        discount_price += (items.product.discount_price * items.quantity)

    tax = round((0.9*discount_price)/100) # calculate tax
    total = discount_price + tax

    context = {
        'cart_items':cart_items,
        'total_price':total_price,
        'discount':discount,
        'tax':tax,
        'total':total,
    }
    return render(request, 'cart/cart.html', context)


@login_required(login_url='login')
def add_to_cart(request, product_slug):
    current_user = request.user
    # 1. Retrieve the Product
    product = get_object_or_404(Product, slug = product_slug) # get the product object by slug.

    cart, created = Cart.objects.get_or_create(user=current_user)
    
    #   IF USER IS LOGGED IN
    if current_user.is_authenticated:

        # 2️. Extract Product Variations (Size, Color, etc.)
        product_variation = []

        if request.method == 'POST':
            for key, value in request.POST.items(): # for loop to get values from user using POST method.
                # (key = 'size' or 'variant' or 'color')
                # value = request.POST[key] | request.POST is a dictionary and returns value coresponding to key.
        
                try:
                    variant = ProductVariant.objects.get(product = product, variant_type__iexact = key, variant_value__iexact = value)
                    product_variation.append(variant)
                except ProductVariant.DoesNotExist:
                    pass


        # 3. check if item exists in cart. 
        cart_items = CartItem.objects.filter(product = product, cart__user = request.user)

        # 4. If the Product Exists, Check Variations.
        if cart_items.exists() : 

            existing_variation_list = [list(item.product_variant.all()) for item in cart_items]
            item_ids = [item.id for item in cart_items]
            print(existing_variation_list)
            print(item_ids)


            if product_variation in existing_variation_list:

                index = existing_variation_list.index(product_variation)
                item = CartItem.objects.get(product = product, id = item_ids[index])
                item.quantity += 1
                item.save()
                messages.success(request, 'Item added to cart')

            # 5. If the Product Exists but with a Different Variation.
            else:   
                
                item = CartItem.objects.create(product = product, quantity = 1, cart=cart)
            

                if len(product_variation) > 0:
                    item.product_variant.add(*product_variation)
                item.save()
                messages.success(request, 'Item added to cart')

        # 6. If the Product Does Not Exist in the Cart.
        else:
            cart_item = CartItem.objects.create(product = product, quantity = 1, cart=cart) # create a new cartItem object 

            if len(product_variation) > 0:
                cart_item.product_variant.add(*product_variation)
            cart_item.save() # save the cartItem object
            messages.success(request, 'Item added to cart')


    return redirect(request.META.get('HTTP_REFERER', 'cart')) # If pressing add to cart from product_detail page REDIRECT to product_detail or redirect to cart.html


@login_required(login_url='login')
def remove(request, product_slug, cart_item_id):
    product = get_object_or_404(Product, slug=product_slug)

    cartitem = get_object_or_404(CartItem, product=product, cart__user = request.user, id=cart_item_id)

    cartitem.delete()

    return redirect('cart')



@login_required(login_url='login')
def decrement_cart_item(request, product_slug, cart_item_id):
    product = get_object_or_404(Product, slug=product_slug)

    cart_item = get_object_or_404(CartItem, product=product, cart__user = request.user,  id=cart_item_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

    return redirect('cart')


@login_required(login_url='login')
def checkout(request):
    total = 0
    
    cartitem = CartItem.objects.filter(cart__user = request.user)

    for item in cartitem:
        total += item.product.discount_price

    # TO view user_adress in checkout.html
    try:
        user_address = UserAddress.objects.filter(user=request.user)[:3]
    except:
        user_address = None 
  

    context = {
        'cart_items':cartitem,
        'total':total,
        'user_address':user_address,
    }
    return render(request, 'order/checkout.html', context)

