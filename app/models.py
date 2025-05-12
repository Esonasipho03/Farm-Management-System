# models.py
from django.db import models
from django.utils import timezone

class Auction(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='auction_images/', default='images/images.jpg', blank=True, null=True)
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2, default = 0.00)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Add default value here
    start_time = models.DateTimeField(null=True, blank=True)  #
    end_time = models.DateTimeField()
    reserve_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.title


class AuctionItem(models.Model):
    auction = models.ForeignKey(Auction, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='crops/', blank=True, null=True)  # Add this line for the image field
    
    def __str__(self):
        return self.name
    
    auction = models.ForeignKey(Auction, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name


class Bid(models.Model):
    auction_item = models.ForeignKey(AuctionItem, related_name='bids', on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Bid Amount: ${self.bid_amount}"
