from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import PaymentForm

import json

# Your Twilio credentials (keep these safe, preferably in environment variables)
TWILIO_ACCOUNT_SID = 'your_account_sid'
TWILIO_AUTH_TOKEN = 'your_auth_token'
TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'

def payment_view(request):
    
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Process the payment details
            print(form.cleaned_data)

            # Get the phone number from the correct field based on the selected payment method
            phone_number = ''
            if form.cleaned_data['payment_method'] == 'CARD':
                phone_number = request.POST.get('payer_phone_number_card')
            elif form.cleaned_data['payment_method'] == 'BANK':
                phone_number = request.POST.get('payer_phone_number_bank')
            elif form.cleaned_data['payment_method'] == 'CAPITEC':
                phone_number = request.POST.get('payer_phone_number_capitec')

            print('Phone Number:', phone_number)

            # Here you might want to save the payment details to the database or perform other actions
            
            return JsonResponse({'status': 'success'})
    else:
        form = PaymentForm()

    return render(request, 'payments/payment.html', {'form': form})


