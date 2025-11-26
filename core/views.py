from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.db import models
from .models import User, Listing, Booking, Vendor, Review, Favorite, UserProfile

# Custom Forms
from .forms import CustomUserCreationForm, ListingForm, VendorProfileForm, UserProfileForm

def home(request):
    # Show featured listings (random 3 or latest 3)
    featured_listings = Listing.objects.all().order_by('-created_at')[:3]
    return render(request, 'home.html', {'featured_listings': featured_listings})

def about(request):
    return render(request, 'about.html')

def listing_list(request):
    listings = Listing.objects.all()
    
    # Search (Title or Description or Cuisine/Tag if we had it)
    query = request.GET.get('q')
    if query:
        listings = listings.filter(
            models.Q(title__icontains=query) | 
            models.Q(description__icontains=query) |
            models.Q(vendor__business_name__icontains=query)
        )
    
    # Filter by Location
    location = request.GET.get('location')
    if location:
        listings = listings.filter(vendor__location__icontains=location)

    # Filter by Price
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    
    if min_price:
        listings = listings.filter(price__gte=min_price)
    if max_price:
        listings = listings.filter(price__lte=max_price)
        
    # Filter by Rating
    min_rating = request.GET.get('min_rating')
    if min_rating:
        listings = listings.annotate(avg_rating=models.Avg('review__rating')).filter(avg_rating__gte=min_rating)
        
    # Get unique locations for the filter dropdown
    locations = Vendor.objects.values_list('location', flat=True).distinct()
        
    return render(request, 'core/listing_list.html', {
        'listings': listings,
        'locations': locations
    })

def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    reviews = Review.objects.filter(listing=listing).order_by('-created_at')
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, listing=listing).exists()
    
    if request.method == 'POST' and 'rating' in request.POST:
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.is_vendor and listing.vendor.user == request.user:
            # Optionally, you can add a message to the user
            messages.error(request, "You cannot review your own listing.")
            return redirect('listing_detail', pk=pk)

        if not request.user.is_tourist:
            messages.error(request, "Only tourists can leave a review.")
            return redirect('listing_detail', pk=pk)
        
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.create(
            user=request.user,
            listing=listing,
            rating=rating,
            comment=comment
        )
        return redirect('listing_detail', pk=pk)
        
    return render(request, 'core/listing_detail.html', {'listing': listing, 'reviews': reviews, 'is_favorite': is_favorite})

@login_required
def payment_page(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if not request.user.is_tourist:
        messages.error(request, "Only tourists can book listings.")
        return redirect('listing_detail', pk=pk)

    if request.method == 'POST':
        date = request.POST.get('date')
        guests = int(request.POST.get('guests'))
        total_price = listing.price * guests
        return render(request, 'core/payment.html', {
            'listing': listing,
            'date': date,
            'guests': guests,
            'total_price': total_price
        })
    return redirect('listing_detail', pk=pk)

@login_required
def process_payment(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == 'POST':
        date = request.POST.get('date')
        guests = request.POST.get('guests')
        # Simulate payment processing... Success!
        booking = Booking.objects.create(
            user=request.user,
            listing=listing,
            date=date,
            guests=guests,
            status='confirmed'
        )
        return redirect('booking_confirmation', pk=booking.pk)
    return redirect('listing_detail', pk=pk)

@login_required
def booking_confirmation(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'core/booking_confirmation.html', {'booking': booking})

@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if booking.status != 'cancelled':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Your booking has been cancelled.')
    else:
        messages.error(request, 'This booking has already been cancelled.')
    return redirect('profile')

@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST' and 'update_picture' in request.POST:
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)

    bookings = Booking.objects.filter(user=request.user).order_by('-date')
    favorite_listings = Listing.objects.filter(favorite__user=request.user)

    return render(request, 'core/profile.html', {
        'form': form,
        'bookings': bookings,
        'favorites': favorite_listings,
        'user_profile': user_profile
    })

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def vendor_dashboard(request):
    if not request.user.is_vendor:
        return redirect('home')
    
    # Ensure vendor profile exists
    vendor, created = Vendor.objects.get_or_create(user=request.user, defaults={
        'business_name': f"{request.user.username}'s Business",
        'description': 'Please update your business description.',
        'location': 'Singapore',
        'contact_number': 'Unknown'
    })
    
    listings = Listing.objects.filter(vendor=request.user.vendor_profile)
    # Fetch bookings for this vendor's listings
    incoming_bookings = Booking.objects.filter(listing__vendor=request.user.vendor_profile).order_by('-date')
    
    return render(request, 'core/vendor_dashboard.html', {
        'listings': listings, 
        'vendor': request.user.vendor_profile,
        'incoming_bookings': incoming_bookings
    })

@login_required
def add_listing(request):
    if not request.user.is_vendor:
        return redirect('home')
    
    vendor = request.user.vendor_profile
    
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.vendor = vendor
            listing.save()
            return redirect('vendor_dashboard')
    else:
        form = ListingForm()
    return render(request, 'core/add_listing.html', {'form': form, 'title': 'Add New Experience'})

@login_required
def edit_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.user != listing.vendor.user:
        return redirect('home')
        
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect('vendor_dashboard')
    else:
        form = ListingForm(instance=listing)
    return render(request, 'core/add_listing.html', {'form': form, 'title': 'Edit Experience'})

@login_required
def delete_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.user == listing.vendor.user:
        listing.delete()
    return redirect('vendor_dashboard')

@login_required
def toggle_favorite(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, listing=listing)
    if not created:
        favorite.delete()
    return redirect('listing_detail', pk=pk)

@login_required
def edit_vendor_profile(request):
    if not request.user.is_vendor:
        return redirect('home')
    
    vendor = request.user.vendor_profile
    
    if request.method == 'POST':
        form = VendorProfileForm(request.POST, request.FILES, instance=vendor)
        if form.is_valid():
            form.save()
            return redirect('vendor_dashboard')
    else:
        form = VendorProfileForm(instance=vendor)
    return render(request, 'core/edit_vendor_profile.html', {'form': form})

class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_vendor:
                return reverse_lazy('vendor_dashboard')
            else:
                return reverse_lazy('profile')
        return reverse_lazy('login')

def vendor_detail(request, pk):
    vendor = get_object_or_404(Vendor, pk=pk)
    listings = Listing.objects.filter(vendor=vendor)
    return render(request, 'core/vendor_detail.html', {'vendor': vendor, 'listings': listings})
