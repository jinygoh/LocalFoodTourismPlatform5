from django import forms
import re
from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import ClearableFileInput

class CustomClearableFileInput(ClearableFileInput):
    template_name = 'core/custom_clearable_file_input.html'
from django.contrib.auth.forms import UserCreationForm
from .models import User, Experience, Shop, UserProfile, Booking, Review
import datetime

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

class TouristUserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input w-full rounded-lg border-border-dark bg-background-dark px-4 py-2.5 text-text-dark focus:border-primary focus:ring-primary'})

class TouristProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['contact_number', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input w-full rounded-lg border-border-dark bg-background-dark px-4 py-2.5 text-text-dark focus:border-primary focus:ring-primary'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']
        widgets = {
            'image': CustomClearableFileInput(attrs={'class': 'form-input w-full text-sm text-text-dark-muted file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-primary/20 file:text-primary hover:file:bg-primary/30'}),
        }

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
        fields = ['business_name', 'description', 'location', 'contact_number', 'opening_hours', 'image', 'dining_establishment_type']

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
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input w-full rounded-lg border-border-dark bg-background-dark px-4 py-2.5 text-text-dark focus:border-primary focus:ring-primary'})

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if date and time:
            booking_datetime = datetime.datetime.combine(date, time)
            if booking_datetime < datetime.datetime.now():
                raise ValidationError("You cannot book a date in the past.")

        if self.shop and self.shop.opening_hours and time:
            try:
                opening_hours_str = self.shop.opening_hours.lower()
                parts = re.split(r'\s*-\s*', opening_hours_str)
                if len(parts) == 2:
                    opening_time_str, closing_time_str = parts
                    opening_time = self.convert_to_24_hour(opening_time_str)
                    closing_time = self.convert_to_24_hour(closing_time_str)

                    if not (opening_time <= time <= closing_time):
                        raise ValidationError(f"The shop is not open at the selected time. Please book between {opening_time_str} and {closing_time_str}.")
                else:
                    raise ValidationError("Could not parse the opening hours. Please contact the shop.")
            except Exception:
                raise ValidationError("Could not parse the opening hours. Please contact the shop.")

        return cleaned_data

    def convert_to_24_hour(self, time_str):
        time_str = time_str.replace(" ", "").lower()

        # Handle "12am" and "12pm"
        if "12am" in time_str:
            time_str = time_str.replace("12am", "00:00")
        elif "12pm" in time_str:
            time_str = time_str.replace("12pm", "12:00")

        # Handle other "am" and "pm" cases
        if "am" in time_str:
            time_str = time_str.replace("am", "")
            if ":" not in time_str:
                time_str += ":00"
        elif "pm" in time_str:
            time_str = time_str.replace("pm", "")
            if ":" not in time_str:
                hour = int(time_str) + 12
                time_str = str(hour) + ":00"
            else:
                parts = time_str.split(":")
                hour = int(parts[0]) + 12
                time_str = str(hour) + ":" + parts[1]

        return datetime.datetime.strptime(time_str, '%H:%M').time()
