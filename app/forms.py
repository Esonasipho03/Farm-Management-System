# forms.py
from django import forms
from .models import Auction, AuctionItem
from django.contrib.auth.models import User




class AuctionForm(forms.ModelForm):
    class Meta:
        model = Auction
        fields = ['title', 'description','image',   'registration_fee', 'current_bid','start_time', 'end_time']

    start_time = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M:%S'],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    end_time = forms.DateTimeField(
        input_formats=['%Y-%m-%d %H:%M:%S'],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )

class AuctionItemForm(forms.ModelForm):
    class Meta:
        model = AuctionItem
        fields = ['name', 'description', 'starting_price', 'image']



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']  # Add any fields you want users to edit
        



