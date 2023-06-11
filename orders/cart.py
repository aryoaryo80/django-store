

CART_SESSION_KEY = 'cart'


class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_KEY)
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add_to_cart(self, product, quantity):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0, 'price': product.price, 'name': product.name, 'total_price': 0}
        self.cart[product_id]['quantity'] += quantity
        self.cart[product_id]['total_price'] = self.cart[product_id]['quantity'] * product.price
        self.session['total'] = sum(item['total_price']
                                    for item in self.cart.values())
        self.save()

    def del_form_cart(self, product_id):
        if str(product_id) in self.cart:
            del self.cart[str(product_id)]
            self.save()

    def __len__(self):
        return len(self.cart)

    def clear(self):
        del self.session[CART_SESSION_KEY]
        self.save()

    def save(self):
        self.session.modified = True
