from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Listing, Vendor, UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_tourist', 'is_vendor')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input w-full rounded-lg border-border-dark bg-background-dark px-4 py-2.5 text-text-dark focus:border-primary focus:ring-primary'})
            field.label_attrs = {'class': 'block text-sm font-medium text-text-dark-muted mb-2'}

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'discount_price', 'image']

class VendorProfileForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['business_name', 'description', 'location', 'contact_number', 'opening_hours', 'image']

