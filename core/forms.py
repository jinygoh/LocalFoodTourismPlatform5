from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import User, Experience, Shop, UserProfile, Booking
import datetime

class TouristProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

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
        fields = ['title', 'description', 'price', 'image']

class ShopProfileForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['business_name', 'description', 'location', 'contact_number', 'opening_hours', 'image']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'time', 'guests']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        self.shop = kwargs.pop('shop', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if date and time:
            booking_datetime = datetime.datetime.combine(date, time)
            if booking_datetime < datetime.datetime.now():
                raise ValidationError("You cannot book a date in the past.")

        if self.shop and self.shop.opening_hours and time:
            opening_hours_str = self.shop.opening_hours.split(': ')[1]
            opening_time_str, closing_time_str = [x.strip() for x in opening_hours_str.split('-')]
            opening_time = datetime.datetime.strptime(opening_time_str, '%I%p').time()
            closing_time = datetime.datetime.strptime(closing_time_str, '%I%p').time()

            if not (opening_time <= time <= closing_time):
                raise ValidationError(f"The shop is not open at the selected time. Please book between {opening_time_str} and {closing_time_str}.")
        return cleaned_data
