from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, EmployeeNumber
from django.core.exceptions import ValidationError
from django import forms
from .models import Crop,Livestock
from .models import  Equipment,Employee
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['name', 'crop_type', 'variety', 'season', 'harvest_date', 'image', 'quantity']
        widgets = {
            'harvest_date': forms.DateInput(attrs={'type': 'date'}),
        }

class LiveForm(forms.ModelForm):
    class Meta:
        model = Livestock
        fields = ['name', 'type' ,'breed','age', 'milkproduction', 'pregnant','weight' ,'healthStatus','image']



        

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']  # Add any fields you want users to edit
        



class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'maintenance_task', 'scheduled_date', 'status']
        widgets = {
            'scheduled_date': forms.DateInput(attrs={'type': 'date'}),
        }

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    user_type = forms.ChoiceField(choices=[('staff', 'Farm Staff'), ('customer', 'Customer')])
    employee_number = forms.CharField(required=False)  # Initially not required
    
    def clean_employee_number(self):
        user_type = self.cleaned_data.get('user_type')
        employee_number = self.cleaned_data.get('employee_number')
        
        if user_type == 'staff':
            if not employee_number:
                raise ValidationError('Employee number is required for farm staff.')
            
            # Check if the employee number exists in the database
            if not EmployeeNumber.objects.filter(employee_number=employee_number).exists():
                raise ValidationError('Invalid employee number.')
        
        return employee_number
    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    
class PasswordResetForm(forms.Form):
    email = forms.EmailField()