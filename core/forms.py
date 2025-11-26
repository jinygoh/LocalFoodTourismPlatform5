from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Listing, Vendor, UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-text-dark-muted file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-primary file:text-white hover:file:bg-primary/90'
            })
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_tourist', 'is_vendor')

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'discount_price', 'image']

class VendorProfileForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['business_name', 'description', 'location', 'contact_number', 'opening_hours', 'image']

