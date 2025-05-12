# urls.py
from django.urls import path
from . import views

urlpatterns = [
   
    
    
    path('auct/', views.auction_list, name='auct_list'),
    path('auctions/create/', views.create_auction, name='create_auction'),
    path('auctions/<int:pk>/edit/', views.update_auction, name='update_auction'),
    path('auct/<int:pk>/', views.auction_detail, name='auct_detail'),
    path('auctions/<int:auction_pk>/items/create/', views.create_auction_item, name='create_auction_item'),
    path('auction/<int:pk>/delete/', views.delete_auction, name='delete_auction'),
    path('auction/<int:auction_pk>/item/<int:item_pk>/delete/', views.delete_auction_item, name='delete_auction_item'),
    
    
]
