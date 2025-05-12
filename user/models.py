from django.db import models
from app.models import Auction, AuctionItem
# Create your models here.

class Auction(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    registration_fee = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='auction_images/', default='auction_images/default.jpg', blank=True, null=True)

class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - R{self.bid_amount} on {self.auction.title}"