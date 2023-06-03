from .cart import Cart


def quantity(request):
    return {
        'cart': Cart(request)
    }
