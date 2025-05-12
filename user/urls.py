from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.homepage, name='homepage'),  # 'homepage' is used in HTML now
    
    path('auction/', views.auctions_list, name='auctions_list'),
     path('account2/', views.account2_view, name='account2'),
    path('auctions/<int:pk>/', views.auctions_detail, name='auctions_detail'),
    path('place_bid/<int:auction_id>/',views.place_bid, name='place_bid'),
     path('thankyou/', views.thankyou_view, name='thankyou'),
    path('delete_bid/<int:bid_id>/',views.delete_bid, name='delete_bid'),
    path('my-bids/', views.user_bids, name='user_bids'),
]