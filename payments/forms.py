from django import forms

class PaymentForm(forms.Form):
    PAYMENT_CHOICES = [
        ('CARD', 'Credit or Cheque Card'),
        ('BANK', 'Pay by Bank'),
        ('CAPITEC', 'Capitec Pay')
    ]
    
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect)
    card_number = forms.CharField(max_length=16, required=False)
    expiry_date = forms.DateField(widget=forms.SelectDateWidget(years=range(2020, 2031)), required=False)
    cvv = forms.CharField(max_length=4, required=False)
