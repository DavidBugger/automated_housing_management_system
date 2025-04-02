from django import forms
from .models import Property,Inquiry

class PropertyForm(forms.ModelForm):
    # image = forms.ImageField()  # Define additional fields outside the Meta class

    class Meta:
        model = Property  # Set the model for the form
        fields = ['property_name', 'color', 'description', 'property_photo',  'property_location', 'price', 'year_built', 'garages', 'plot_size', 'area', 'bathroom', 'bedroom']  # Use a list or tuple
        
class PropertyEditForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['property_name', 'property_photo', 'property_location', 'year_built', 'price', 
                  'garages', 'plot_size', 'area', 'bathroom', 'bedroom', 'color', 'description', 'is_sold']



class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'name',
                'placeholder': 'Name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'email',
                'placeholder': 'Email',
                'required': True
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'phone',
                'placeholder': 'Phone',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'msg',
                'placeholder': 'Write a Message',
                'rows': 4,
                'required': True
            }),
        }
