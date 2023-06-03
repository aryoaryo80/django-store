from django.urls import path
from . import views


app_name = 'orders'
urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/<slug:product_slug>/',
         views.AddToCartView.as_view(), name='add_to_cart'),
    path('cart/del/<int:product_id>/',
         views.DelFromCart.as_view(), name='del_from_cart'),
    path('create/', views.CreateOrderView.as_view(), name='create_order'),
    path('detail/<int:order_id>/',
         views.OrderDetailView.as_view(), name='order_detail'),
    path('apply/<int:order_id>', views.OrderDetailView.as_view(), name='apply_order'),
]
