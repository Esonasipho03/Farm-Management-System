from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image')  # Display the image field in admin

admin.site.register(Product, ProductAdmin)

