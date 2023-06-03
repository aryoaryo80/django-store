from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from home.models import *
from home.forms import *
from .models import *
from .cart import Cart
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime


class CartView(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            orders = Order.objects.filter(user=request.user)
            if orders.exists():
                return render(request, 'orders/cart.html', {'orders': orders})
        return render(request, 'orders/cart.html')


class AddToCartView(View):

    def post(self, request, *args, **kwargs):
        form = AddToCartForm(request.POST)
        product = get_object_or_404(Product, slug=kwargs['product_slug'])
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            cart = Cart(request)
            cart.add_to_cart(product, quantity)
            messages.success(request, 'Added to cart successfully')
            return redirect(product.get_absolute_url())

        return render(request, 'home/product_detail.html', {'product': product, 'form': form})


class DelFromCart(View):

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        # get_object_or_404(Product, slug=kwargs['product_id'])
        cart.del_form_cart(kwargs['product_id'])
        messages.warning(request, 'product deleted form your cart', 'warning')
        return redirect('orders:cart')


class CreateOrderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cart = request.session['cart']
        if len(cart):
            order = Order.objects.create(user=request.user)
            for key, value in cart.items():
                product = get_object_or_404(Product, id=key)
                OrderItem.objects.create(
                    order=order, product=product, price=product.price, quantity=value['quantity'])
            Cart(request).clear()
            messages.success(request, 'order created successfully')
            return redirect('orders:order_detail', order.id)
        messages.success(request, 'your cart is empty', 'warning')
        return redirect('orders:cart')


class OrderDetailView(LoginRequiredMixin, View):
    form_class = CouponApplyForm

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs['order_id'])
        return render(request, 'orders/order_detail.html', {'order': order, 'form': self.form_class})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        order = get_object_or_404(Order, pk=kwargs['order_id'])
        if form.is_valid():
            code = form.cleaned_data['code']
            now = datetime.utcnow()
            coupon = Coupon.objects.filter(
                code=code, active=True, valid_from__lt=now, valid_to__gt=now)
            if coupon.exists():
                order.discount = coupon[0].discount
                order.save()
                messages.success(request, 'Coupon applied successfully')
                return redirect('orders:order_detail', order.id)
            messages.error(request, 'Coupon is not correct', 'danger')
            return redirect('orders:order_detail', order.id)
        return render(request, 'orders/order_detail.html', {'order': order, 'form': form})
