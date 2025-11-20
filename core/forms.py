from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Listing

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_tourist', 'is_vendor')

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'discount_price', 'image']

