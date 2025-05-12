from django.contrib.auth.models import User
from django.db import models


class EmployeeNumber(models.Model):
    employee_number = models.CharField(max_length=10)

    def __str__(self):
        return self.employee_number

class UserProfile(models.Model):
    USER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('staff', 'Farm Staff'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    employee_number = models.ForeignKey('EmployeeNumber', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Crop(models.Model):
    # Define choices for crop types
    CROP_TYPES = [
        ('Grain', 'Grain'),
        ('Vegetable', 'Vegetable'),
        ('Fruit', 'Fruit'),
        ('Legume', 'Legume'),
        ('Tubers', 'Tubers'),
    ]

    # Define choices for varieties
    VARIETIES = [
        ('Wheat', 'Wheat'),
        ('Rice', 'Rice'),
        ('Barley', 'Barley'),
        ('Carrot', 'Carrot'),
        ('Spinach', 'Spinach'),
        ('Broccoli', 'Broccoli'),
        ('Apple', 'Apple'),
        ('Banana', 'Banana'),
        ('Orange', 'Orange'),
        ('Peas', 'Peas'),
        ('Lentils', 'Lentils'),
        ('Beans', 'Beans'),
        ('Potato', 'Potato'),
        ('Sweet Potato', 'Sweet Potato'),
        ('Yam', 'Yam'),
        ('Grapes','Grapes'),
    ]

    name = models.CharField(max_length=100)
    crop_type = models.CharField(max_length=50, choices=CROP_TYPES)  # Select crop type from predefined choices
    variety = models.CharField(max_length=50, choices=VARIETIES, blank=True)  # Variety choices based on all types
    season = models.CharField(max_length=50)
    harvest_date = models.DateField()
    image = models.ImageField(upload_to='crops/', blank=True, null=True)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    
    
    
class Livestock(models.Model):
    LIVESTOCK_TYPES = [
        ('Cattle', 'Cattle'),
        ('Sheep', 'Sheep'),
        ('Pigs', 'Pigs'),
        ('Goats', 'Goats'),
        ('Horses', 'Horses'),
    ]
    BREEDS = {
        'Cattle': [
            ('Angus', 'Angus'),
            ('Hereford', 'Hereford'),
            ('Holstein', 'Holstein'),
            ('Jersey', 'Jersey'),
        ],
        'Sheep': [
            ('Merino', 'Merino'),
            ('Suffolk', 'Suffolk'),
            ('Dorset', 'Dorset'),
            ('Hampshire', 'Hampshire'),
        ],
        'Pigs': [
            ('Yorkshire', 'Yorkshire'),
            ('Berkshire', 'Berkshire'),
            ('Landrace', 'Landrace'),
            ('Duroc', 'Duroc'),
        ],
        'Goats': [
            ('Nubian', 'Nubian'),
            ('Boer', 'Boer'),
            ('Alpine', 'Alpine'),
            ('Saanen', 'Saanen'),
        ],
        'Horses': [
            ('Arabian', 'Arabian'),
            ('Clydesdale', 'Clydesdale'),
            ('Thoroughbred', 'Thoroughbred'),
            ('Quarter Horse', 'Quarter Horse'),
        ],
    }
    
    type = models.CharField(max_length=20, choices=LIVESTOCK_TYPES)
    breed = models.CharField(max_length=20, blank=True)
    
    # Other fields
    name = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=10, decimal_places=2, default=0.0, blank=True)
    milkproduction = models.DecimalField(max_digits=10, decimal_places=2)
    pregnant = models.CharField(max_length=100)
    healthStatus = models.TextField(max_length=100)
    image = models.ImageField(upload_to='crops/', blank=True, null=True)

    def clean(self):
        # Set breed choices based on type
        if self.type in self.BREEDS:
            self._meta.get_field('breed').choices = self.BREEDS[self.type]
        else:
            self._meta.get_field('breed').choices = []
        super().clean()

    def __str__(self):
        return self.name


class Equipment(models.Model):
    EQUIPMENT_TASK_CHOICES = [
        ('Check-up', 'Check-up'),
        ('Servicing', 'Servicing'),
        ('Replacement', 'Replacement'),
    ]
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]
    
    name = models.CharField(max_length=100)
    maintenance_task = models.CharField(max_length=50, choices=EQUIPMENT_TASK_CHOICES)
    scheduled_date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    def __str__(self):
        return self.name

class Employee(models.Model):
    employee_number = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.employee_number


from shop.models import Product

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_id = models.CharField(max_length=100)
    purchase_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.product.name} - {self.order_id}'