from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Experience, Shop, UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']

class CustomUserCreationForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('tourist', 'Tourist'),
        ('vendor', 'Vendor'),
    )
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        required=True,
        label="Are you a tourist or a vendor?"
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'user_type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'user_type':
                field.widget.attrs.update({
                    'class': 'form-input w-full rounded-lg border-border-dark bg-background-dark px-4 py-2.5 text-text-dark focus:border-primary focus:ring-primary'
                })

    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        if user_type == 'tourist':
            self.instance.is_tourist = True
        elif user_type == 'vendor':
            self.instance.is_vendor = True
        return cleaned_data

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'description', 'price', 'discount_price', 'image']

class ShopProfileForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['business_name', 'description', 'location', 'contact_number', 'opening_hours', 'image']
