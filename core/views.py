from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import User, Listing, Booking, Vendor, Review, Favorite

# Custom Forms
from .forms import CustomUserCreationForm, ListingForm

def home(request):
    # Show featured listings (random 3 or latest 3)
    featured_listings = Listing.objects.all().order_by('-created_at')[:3]
    return render(request, 'home.html', {'featured_listings': featured_listings})

def about(request):
    return render(request, 'about.html')

def listing_list(request):
    listings = Listing.objects.all()
    # Simple search
    query = request.GET.get('q')
    if query:
        listings = listings.filter(title__icontains=query)
    return render(request, 'core/listing_list.html', {'listings': listings})

def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    reviews = Review.objects.filter(listing=listing).order_by('-created_at')
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, listing=listing).exists()
    
    if request.method == 'POST' and 'rating' in request.POST:
        if not request.user.is_authenticated:
            return redirect('login')
        
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
        Booking.objects.create(
            user=request.user,
            listing=listing,
            date=date,
            guests=guests,
            status='confirmed'
        )
        return redirect('profile')
    return redirect('listing_detail', pk=pk)

@login_required
def profile(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-date')
    favorites = Favorite.objects.filter(user=request.user).select_related('listing')
    return render(request, 'core/profile.html', {'bookings': bookings, 'favorites': favorites})

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
    
    listings = Listing.objects.filter(vendor=vendor)
    # Fetch bookings for this vendor's listings
    incoming_bookings = Booking.objects.filter(listing__vendor=vendor).order_by('-date')
    
    return render(request, 'core/vendor_dashboard.html', {
        'listings': listings, 
        'vendor': vendor,
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
