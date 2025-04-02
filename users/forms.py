
from typing import Self
from django import forms 
from .models import Location, Profile

from django.contrib.auth.models import User

# from localflavor.us.models import USStateField, USZipCodeField



class UserForm(forms.ModelForm):
    username = forms.CharField(disabled=True)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
        
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo', 'bio', 'phone_number')

class LocationForm(forms.ModelForm):
    address_1 = forms.CharField(required=True)
    zip_code = forms.CharField(required=True)
    # def clean_zip_code(self):
    #     zip_code = self.cleaned_data.get(zip_code')
    #     if not zip_code:
    #         raise forms.ValidationError('Zip Code is required')
    #     return zip_code
    
    class Meta:
        model = Location
        fields = {'address_1', 'address_2', 'city', 'state', 'zip_code'}
        
    
    