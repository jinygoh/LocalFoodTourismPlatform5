#
# This file (`core/forms.py`) defines the forms used throughout the TasteLocal application.
# Django forms handle rendering HTML form elements, validating user-submitted data,
# and converting that data into Python types.
#
# These forms are used by the views (`core/views.py`) to handle user input for actions
# like registration, creating reviews, booking experiences, and editing profiles.
# `ModelForm` is heavily used, which automatically creates form fields based on
# a corresponding Django model (`core/models.py`).
#
from django import forms
import re
from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import ClearableFileInput
from django.contrib.auth.forms import UserCreationForm
from .models import User, Experience, Shop, UserProfile, Booking, Review, Dish
import datetime

#
# A custom widget to render a file input with a more appealing style.
# It uses a custom HTML template for rendering.
#
class CustomClearableFileInput(ClearableFileInput):
    template_name = 'core/custom_clearable_file_input.html'

#
# Form for creating or updating a Review.
# It's a ModelForm linked to the Review model.
#
class ReviewForm(forms.ModelForm):
    # Meta class defines which model to use and which fields to include.
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
        }

    # The __init__ method is used to customize the form fields, in this case,
    # to add CSS classes for styling.
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update({
            'class': 'form-input w-full rounded-lg border-border-dark bg-background-dark px-4 py-2.5 text-text-dark focus:border-primary focus:ring-primary',
        })
        self.fields['comment'].widget.attrs.update({
            'class': 'form-input w-full rounded-lg border-border-dark bg-background-dark px-4 py-2.5 text-text-dark focus:border-primary focus:ring-primary',
            'rows': 4,
        })

#
# Form for editing the core details of a User model (for tourists).
#
class TouristUserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Loop through all fields to apply a consistent CSS class for styling.
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input w-full rounded-lg border-border-dark bg-background-dark px-4 py-2.5 text-text-dark focus:border-primary focus:ring-primary'})

#
# Form for editing the UserProfile model (for tourists).
#
class TouristProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['contact_number', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input w-full rounded-lg border-border-dark bg-background-dark px-4 py-2.5 text-text-dark focus:border-primary focus:ring-primary'})

#
# Form specifically for updating a user's profile image.
#
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']
        widgets = {
            # Uses the custom file input widget for better styling.
            'image': CustomClearableFileInput(attrs={'class': 'form-input w-full text-sm text-text-dark-muted file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-primary/20 file:text-primary hover:file:bg-primary/30'}),
        }

#
# A custom user registration form that extends Django's default UserCreationForm.
# It adds a 'user_type' field to distinguish between tourists and vendors.
#
class CustomUserCreationForm(UserCreationForm):
    # Choices for the user type radio buttons.
    USER_TYPE_CHOICES = (
        ('tourist', 'Tourist'),
        ('vendor', 'Vendor'),
    )
    # The new field for selecting user type.
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.RadioSelect, # Renders as radio buttons.
        required=True,
        label="Are you a tourist or a vendor?"
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'user_type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply styling to all fields except the radio buttons.
        for field_name, field in self.fields.items():
            if field_name != 'user_type':
                field.widget.attrs.update({
                    'class': 'form-input w-full rounded-lg border-border-dark bg-background-dark px-4 py-2.5 text-text-dark focus:border-primary focus:ring-primary'
                })

    # The clean method is used for custom validation that can involve multiple fields.
    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        # Based on the user_type selection, set the boolean flags on the User instance.
        if user_type == 'tourist':
            self.instance.is_tourist = True
        elif user_type == 'vendor':
            self.instance.is_vendor = True
        return cleaned_data

#
# Form for creating or updating an Experience listing.
#
class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'description', 'price', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input w-full rounded-lg border-border-dark bg-background-dark px-4 py-2.5 text-text-dark focus:border-primary focus:ring-primary'})

#
# Form for creating or updating a Dish listing.
#
class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['name', 'description', 'price', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input w-full rounded-lg border-border-dark bg-background-dark px-4 py-2.5 text-text-dark focus:border-primary focus:ring-primary'})

#
# Form for editing a vendor's Shop profile.
#
class ShopProfileForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ['business_name', 'description', 'location', 'contact_number', 'opening_hours', 'image', 'dining_establishment_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input w-full rounded-lg border-border-dark bg-background-dark px-4 py-2.5 text-text-dark focus:border-primary focus:ring-primary'})

#
# Form for creating a Booking.
#
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'time', 'guests']
        widgets = {
            # Use HTML5 date and time inputs for a better user experience.
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        # The shop is passed in from the view to be used in custom validation.
        self.shop = kwargs.pop('shop', None)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-input w-full rounded-lg border-border-dark bg-background-dark px-4 py-2.5 text-text-dark focus:border-primary focus:ring-primary'})

    # Custom validation for the booking form.
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        # Check 1: Ensure the booking is not in the past.
        if date and time:
            booking_datetime = datetime.datetime.combine(date, time)
            if booking_datetime < datetime.datetime.now():
                raise ValidationError("You cannot book a date in the past.")

        # Check 2: Ensure the booking is within the shop's opening hours.
        if self.shop and time:
            day_of_week = date.isoweekday() # Monday is 1 and Sunday is 7
            is_open = False

            # Check against the structured opening hours data.
            if self.shop.opening_hours_structured:
                for slot in self.shop.opening_hours_structured:
                    if slot['day_of_week'] == day_of_week:
                        open_time = datetime.datetime.strptime(slot['open_time'], '%H:%M').time()
                        close_time = datetime.datetime.strptime(slot['close_time'], '%H:%M').time()
                        if open_time <= time <= close_time:
                            is_open = True
                            break

            if not is_open:
                raise ValidationError("You must book a time during the shop's opening hours.")

        return cleaned_data
