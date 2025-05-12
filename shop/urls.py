from django.urls import path
from . import views

urlpatterns = [
    
    path('shop/', views.shop_view, name='shop'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/update/<str:product_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<str:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    
    path('payment/', views.payment_view, name='payment'),
    
    path('successful_payment/', views.successful_payment, name='successful_payment'),
  
    path('auctions/', views.auctionpage, name='auctionspage'),
    
    
]


    



















    