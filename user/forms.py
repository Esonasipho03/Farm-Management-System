from django import forms
from .models import Bid

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['name', 'phone', 'bid_amount']

        widgets = {
            'name': forms.TextInput(attrs={'required': True}),
            'phone': forms.TextInput(attrs={'type': 'tel', 'pattern': '[0-9]{10}', 'required': True}),
            'bid_amount': forms.NumberInput(attrs={'min': 0, 'required': True}),
        }

    def __init__(self, *args, **kwargs):
        auction = kwargs.pop('auction', None)
        super(BidForm, self).__init__(*args, **kwargs)
        if auction:
            self.fields['bid_amount'].widget.attrs['min'] = auction.current_bid
