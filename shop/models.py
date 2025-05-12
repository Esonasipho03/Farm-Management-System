from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')  # Add an ImageField to store product images
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order of {self.product.name} (x{self.quantity})"
    
class Payment(models.Model):
    PAYMENT_METHODS = [
        ('CARD', 'Credit or Cheque Card'),
        ('BANK', 'Pay by Bank'),
        ('CAPITEC', 'Capitec Pay')
    ]
    
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    card_number = models.CharField(max_length=16, blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    cvv = models.CharField(max_length=4, blank=True, null=True)

    def __str__(self):
        return self.payment_method
