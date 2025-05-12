from django.urls import reverse
from django.shortcuts import render, redirect , get_object_or_404
from .models import Product, Order
from django.http import HttpResponse
from django.conf import settings

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import PaymentForm

import json
from decimal import Decimal
from django.core.mail import send_mail


from django.db.models import Q
from .models import Product


# Homepage view with breadcrumbs
def homepage(request):
    query = request.GET.get('q')  # Get the search query
    breadcrumbs = [
        {'name': 'Home', 'url': reverse('homepage')},
    ]
    return render(request, 'index.html', {'breadcrumbs': breadcrumbs})

# Shop view with breadcrumbs
def shop_view(request):
    query = request.GET.get('q')  # Get the search query
    print(f"Search query: {query}")  # Debug: Print the query

    if query:
        products = Product.objects.filter(name__icontains=query)  # Filter products by name
        print(f"Filtered products: {products}")  # Debug: Print filtered products
    else:
        products = Product.objects.all()

    breadcrumbs = [
        {'name': 'Home', 'url': reverse('homepage')},
        {'name': 'Shop', 'url': reverse('shop')}
    ]
    
    return render(request, 'shop/shop.html', {'products': products, 'breadcrumbs': breadcrumbs})



# Add to cart view with breadcrumbs
def add_to_cart(request, product_id):
    query = request.GET.get('q')  # Get the search query
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {
            'name': product.name,
            'price': str(product.price),
            'quantity': 1,
            'available_stock': product.stock,
            'image_url': product.image.url
        }
    request.session['cart'] = cart
    return redirect(f'{reverse("shop")}?added_to_cart=true')

# Cart view with breadcrumbs
def cart_view(request):
    query = request.GET.get('q')  # Get the search query
    cart = request.session.get('cart', {})
    total_price = Decimal('0.00')
    breadcrumbs = [
        {'name': 'Home', 'url': reverse('homepage')},
        {'name': 'Cart', 'url': reverse('cart')}
    ]

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        quantity = int(request.POST.get('quantity', 1))

        if action == 'remove':
            if product_id in cart:
                del cart[product_id]
        elif action == 'update':
            if product_id in cart:
                cart[product_id]['quantity'] = quantity

        request.session['cart'] = cart
        return redirect('cart')

    for product_id, details in cart.items():
        details['total'] = Decimal(details['price']) * details['quantity']
        total_price += details['total']

    context = {
        'cart': cart,
        'total_price': total_price,
        'breadcrumbs': breadcrumbs
    }
    return render(request, 'shop/cart.html', context)

def update_cart(request, product_id):
    query = request.GET.get('q')  # Get the search query
    cart = request.session.get('cart', {})
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity'))
        cart = request.session.get('cart', {})
        if product_id in cart:
            cart[product_id]['quantity'] = quantity
            request.session['cart'] = cart
    return redirect('cart')

def remove_from_cart(request, product_id):
    query = request.GET.get('q')  # Get the search query
    cart = request.session.get('cart', {})
    if request.method == 'POST':
        if product_id in cart:
            del cart[product_id]
            request.session['cart'] = cart
    return redirect('cart')

 
 # Checkout view with breadcrumbs
def checkout_view(request):
    query = request.GET.get('q')  # Get the search query
    cart = request.session.get('cart', {})
    total_price = 0
    order_items = []
    errors = []
    breadcrumbs = [
        {'name': 'Home', 'url': reverse('homepage')},
        {'name': 'Checkout', 'url': reverse('checkout')}
    ]

    for product_id, item in cart.items():
        product = Product.objects.get(id=product_id)
        quantity = item['quantity']
        if quantity > product.stock:
            errors.append(f"Sorry, {product.name} only has {product.stock} left in stock.")
        else:
            total_price += float(item['price']) * quantity
            order_items.append({
                'product': product,
                'quantity': quantity,
                'price': item['price']
            })

    if errors:
        return render(request, 'shop/checkout.html', {'order_items': order_items, 'total_price': total_price, 'errors': errors, 'breadcrumbs': breadcrumbs})

    if request.method == 'POST':
        for item in order_items:
            product = item['product']
            quantity = item['quantity']
            total_price = float(item['price']) * quantity
            Order.objects.create(product=product, quantity=quantity, total_price=total_price)
            product.stock -= quantity
            product.save()

        request.session['cart'] = {}
        return redirect('payment')

    return render(request, 'shop/checkout.html', {'order_items': order_items, 'total_price': total_price, 'breadcrumbs': breadcrumbs})


from signup.models import Purchase

def successful_payment(request):
    order_id = request.GET.get('order_id', None)
    cart_products = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart_products)

    # Get the current user’s email
    user_email = request.user.email

    # Record the purchase
    for product in products:
        Purchase.objects.create(
            user=request.user,
            product=product,
            quantity=1,  # Adjust this based on the cart structure
            total_price=product.price,
            order_id=order_id
        )

    # Email confirmation logic
    if request.method == 'POST':
        subject = 'Order Confirmation'
        message = f'Thank you for your payment!\n\nOrder ID: {order_id}\nProducts:\n'
        for product in products:
            message += f'{product.name} - R{product.price}\n'
        message += '\nYour order will be delivered soon.'
        
        recipient_list = [user_email]
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

    return render(request, 'shop/successful_payment.html', {
        'order_id': order_id,
        'products': products,
    })

# Payment options view with breadcrumbs
def payment_view(request):
    query = request.GET.get('q')  # Get the search query
    breadcrumbs = [
        {'name': 'Home', 'url': reverse('homepage')},
        {'name': 'Checkout', 'url': reverse('checkout')},
        {'name': 'Payment Options', 'url': reverse('payment')}
    ]

    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Process the payment details
            print(form.cleaned_data)

            # Get the email from the correct field based on the selected payment method
            email = ''
            if form.cleaned_data['payment_method'] == 'CARD':
                email = request.POST.get('payer_email_card')
            elif form.cleaned_data['payment_method'] == 'BANK':
                email = request.POST.get('payer_email_bank')
            elif form.cleaned_data['payment_method'] == 'CAPITEC':
                email = request.POST.get('payer_email_capitec')

            print('Email:', email)

            # Send a confirmation email
            send_mail(
                'Payment Confirmation',
                'You will receive your order details once your payment has been received.',
                'no-reply@yourdomain.com',  # From email
                [email],  # To email
                fail_silently=False,
            )

            return JsonResponse({'status': 'success'})
    else:
        form = PaymentForm()

    return render(request, 'shop/payment.html', {'form': form, 'breadcrumbs': breadcrumbs})




    


def auctionpage(request):
    query = request.GET.get('q')  # Get the search query
    return render(request, 'auctions.html')

