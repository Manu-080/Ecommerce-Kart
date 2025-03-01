from .models import CartItem


def get_quantity(request, quantity=0):
    try:
        cartitem = CartItem.objects.filter(cart__user = request.user)

        for item in cartitem:
            if item.product.stock > 0:
                quantity += item.quantity
    except:
        cartitem = None

    return {'total_quantity':quantity}
