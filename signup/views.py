

from django.contrib.auth import login
from .models import Purchase, UserProfile
from django.shortcuts import render, redirect, get_object_or_404
from .models import Crop,Livestock,Equipment,EmployeeNumber
from .forms import CropForm,LiveForm,UserProfileForm,EquipmentForm,SignUpForm,LoginForm,PasswordResetForm
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from user.models import Auction
from shop.models import Product
from django.db.models import Count
from .models import Crop
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth.forms import SetPasswordForm
from django.utils.http import urlsafe_base64_decode


def landing_page(request):
    return render(request, 'landing_page.html')

def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                # Generate token and uid
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                # Create the password reset link
                reset_link = f"{request.scheme}://{request.get_host()}/reset/{uid}/{token}/"
                # Prepare email
                subject = "Password Reset Requested"
                message = render_to_string('password_reset_email.html', {
                    'reset_link': reset_link,
                    'user': user,
                })
                send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
                messages.success(request, "Password reset email has been sent.")
            except User.DoesNotExist:
                messages.error(request, "Email address not found.")
        return redirect('password_reset_request')
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset_request.html', {'form': form})

def password_reset_confirm(request, uidb64, token):
    try:
        user = User.objects.get(pk=urlsafe_base64_decode(uidb64).decode())
        if default_token_generator.check_token(user, token):
            if request.method == "POST":
                form = SetPasswordForm(user, request.POST)
                if form.is_valid():
                    user = form.save()
                    messages.success(request, "Your password has been set. You can now log in.")
                    return redirect('login')
            else:
                form = SetPasswordForm(user)
        else:
            messages.error(request, "The password reset link is invalid.")
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    return render(request, 'password_reset_confirm.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user_type = form.cleaned_data['user_type']
            employee_number_str = form.cleaned_data.get('employee_number')

            if user_type == 'staff' and not employee_number_str:
                messages.error(request, 'Employee number is required for staff.')
                return render(request, 'signup.html', {'form': form})

            if user_type == 'staff':
                try:
                    employee_instance = EmployeeNumber.objects.get(employee_number=employee_number_str)
                except EmployeeNumber.DoesNotExist:
                    messages.error(request, 'Invalid employee number.')
                    return render(request, 'signup.html', {'form': form})

            # Create the user
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                email=form.cleaned_data['email']
            )

            # Create user profile
            UserProfile.objects.create(
                user=user,
                user_type=user_type,
                employee_number=employee_instance if user_type == 'staff' else None,
            )

            # Send confirmation email
            subject = 'Welcome to GreenFarm!'
            message = f'Hi {user.username},\n\nYour account has been successfully created.'
            recipient_list = [user.email]
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)

            return redirect('login')  # Redirect after successful signup
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.userprofile.user_type == 'staff':
                    return redirect('management_home')
                else:
                    return redirect('homepage')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'customer_login.html', {'form': form})
    


# Custom login view for customers
from datetime import datetime

def management_home(request):
    today = datetime.today().date()
    # Fetch equipment due for maintenance soon
    upcoming_maintenance = Equipment.objects.filter(scheduled_date__gte=today)

    # Pass the relevant fields to the template
    return render(request, 'managementhome.html', {
        'upcoming_maintenance': upcoming_maintenance,
    })

# Display crops
def crop_list(request):
    query = request.GET.get('q')  # Get the search query
    if query:
        crops = Crop.objects.filter(name__icontains=query)  # Filter crops by name
    else:
        crops = Crop.objects.all()

    breadcrumbs = [
        {'name': 'Home', 'url': '/'},
        {'name': 'Crops', 'url': ''},
    ]
    
    return render(request, 'crop_list.html', {'crops': crops, 'breadcrumbs': breadcrumbs})


# View details of a single crop
def crop_detail(request, pk):
    crop = get_object_or_404(Crop, pk=pk)
    breadcrumbs = [
        {'name': 'Home', 'url': '/'},
        {'name': 'Crops', 'url': '/crops/'},
        {'name': crop.name, 'url': ''}
    ]
    return render(request, 'crop_detail.html', {'crop': crop, 'breadcrumbs': breadcrumbs})

# Add or edit a crop
def crop_edit(request, pk=None):
    crop = get_object_or_404(Crop, pk=pk) if pk else None
    if request.method == "POST":
        form = CropForm(request.POST, request.FILES, instance=crop)
        if form.is_valid():
            form.save()
            return redirect('crop_list')
    else:
        form = CropForm(instance=crop)
    return render(request, 'crop_edit.html', {'form': form})

# Delete a crop
def crop_delete(request, pk):
    crop = get_object_or_404(Crop, pk=pk)
    if request.method == "POST":
        crop.delete()
        return redirect('crop_list')
    return render(request, 'crop_confirm_delete.html', {'crop': crop})




# Display Livestock
def live_list(request):
    query = request.GET.get('q')  # Get the search query
    if query:
        livestock_list = Livestock.objects.filter(name__icontains=query)  # Filter livestock by name
    else:
        livestock_list = Livestock.objects.all()

    breadcrumbs = [
        {'name': 'Home', 'url': '/'},
        {'name': 'Livestock', 'url': ''},
    ]
    
    return render(request, 'live_list.html', {'live': livestock_list, 'breadcrumbs': breadcrumbs})



# View details of a single livestock
def live_detail(request, pk):
    live = get_object_or_404(Livestock, pk=pk)
    breadcrumbs = [
        {'name': 'Home', 'url': '/'},
        {'name': 'Livestock', 'url': '/live/'},
        {'name': live.name, 'url': ''}
    ]
    return render(request, 'live_detail.html', {'live': live, 'breadcrumbs': breadcrumbs})

# Add or edit a livestock
def live_edit(request, pk=None):
    if pk:
        # Editing existing livestock
        livestock = get_object_or_404(Livestock, pk=pk)
        if request.method == 'POST':
            form = LiveForm(request.POST, request.FILES, instance=livestock)
            if form.is_valid():
                form.save()
                return redirect('live_list')
        else:
            form = LiveForm(instance=livestock)
    else:
        # Adding new livestock
        if request.method == 'POST':
            form = LiveForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('live_list')
        else:
            form = LiveForm()

    return render(request, 'live_edit.html', {'form': form})

# Delete a livestock
def live_delete(request, pk):
    live = get_object_or_404(Livestock, pk=pk)
    if request.method == "POST":
        live.delete()
        return redirect('live_list')
    return render(request, 'clive_confirm_delete.html', {'live': live})

def search_view(request):
    query = request.GET.get('q')  # Get the search query
    category = request.GET.get('category')  # Get the category (e.g., 'crops', 'livestock', 'auctions', 'products')

    crops = livestock = auctions = products = None  # Initialize variables

    if category == 'crops':
        crops = Crop.objects.filter(name__icontains=query)
    elif category == 'livestock':
        livestock = Livestock.objects.filter(name__icontains=query)
    elif category == 'auctions':
        auctions = Auction.objects.filter(title__icontains=query)  # Correct field name 'title'
    elif category == 'products':
        products = Product.objects.filter(name__icontains=query)

    context = {
        'query': query,
        'category': category,
        'crops': crops,
        'livestock': livestock,
        'auctions': auctions,
        'products': products,
    }

    return render(request, 'search_results.html', context)
def account_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account')  # Redirect to account page after successful update
    else:
        form = UserProfileForm(instance=user)
    
    context = {
        'form': form,
        'user': user,
    }
    return render(request, 'account.html', context)





def equipment_schedule(request):
    equipment_list = Equipment.objects.all()
    
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)  # Log the form data to check what's being captured
            form.save()
            return redirect('schedule')
    else:
        form = EquipmentForm()

    context = {
        'equipment_list': equipment_list,
        'form': form,
    }
    return render(request, 'equipment_schedule.html', context)

def edit_equipment(request, pk):
    equipment = Equipment.objects.get(pk=pk)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            return redirect('equipment_schedule')
    else:
        form = EquipmentForm(instance=equipment)

    context = {
        'form': form,
        'equipment': equipment,
    }
    return render(request, 'edit_equipment.html', context)

def livestock_inventory_report(request):
    livestock = Livestock.objects.all()
    livestock_by_type = livestock.values('type').annotate(total=Count('type'))
    livestock_by_breed = livestock.values('breed').annotate(total=Count('breed'))
    
    context = {
        'livestock_by_type': livestock_by_type,
        'livestock_by_breed': livestock_by_breed,
    }
    return render(request, 'livestock_inventory_report.html', context)





from django.db.models import Sum  # Import Sum for aggregation
from django.shortcuts import render
from .models import Crop  # Ensure your Crop model is imported

def crop_inventory_report(request):
    # Query to get crops grouped by variety and type, with aggregated quantities
    crops_by_variety = Crop.objects.values('variety').annotate(total_quantity=Sum('quantity'))
    crops_by_type = Crop.objects.values('crop_type').annotate(total_quantity=Sum('quantity'))

    return render(request, 'crop_inventory_report.html', {
        'crops_by_variety': crops_by_variety,
        'crops_by_type': crops_by_type
    })
    
   

from django.contrib.admin.views.decorators import staff_member_required
@staff_member_required
def purchase_report(request):
    purchases = Purchase.objects.all().order_by('-purchase_date')

    return render(request, 'signup/livestock_inventory_report.html', {
        'purchases': purchases,
    })