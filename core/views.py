from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.db.models import Q, Avg
from django.contrib.contenttypes.models import ContentType
from .models import User, Experience, Booking, Shop, Review, Favorite, UserProfile, Dish

# Custom Forms
from .forms import CustomUserCreationForm, ExperienceForm, ShopProfileForm, UserProfileForm

def home(request):
    featured_experiences = Experience.objects.all().order_by('-created_at')[:3]
    return render(request, 'home.html', {'featured_experiences': featured_experiences})

def about(request):
    return render(request, 'about.html')

def explore(request):
    query = request.GET.get('q')
    location = request.GET.get('location')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_rating = request.GET.get('min_rating')

    experiences = Experience.objects.all()
    shops = Shop.objects.all()
    dishes = Dish.objects.all()

    if query:
        experiences = experiences.filter(Q(title__icontains=query) | Q(description__icontains=query))
        shops = shops.filter(Q(business_name__icontains=query) | Q(description__icontains=query))
        dishes = dishes.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if location:
        experiences = experiences.filter(vendor__location__icontains=location)
        shops = shops.filter(location__icontains=location)

    if min_price:
        experiences = experiences.filter(price__gte=min_price)
    if max_price:
        experiences = experiences.filter(price__lte=max_price)

    if min_rating:
        experiences = experiences.annotate(avg_rating=Avg('review__rating')).filter(avg_rating__gte=min_rating)
        shops = shops.annotate(avg_rating=Avg('review__rating')).filter(avg_rating__gte=min_rating)
        dishes = dishes.annotate(avg_rating=Avg('review__rating')).filter(avg_rating__gte=min_rating)
        
    locations = Shop.objects.values_list('location', flat=True).distinct()

    return render(request, 'core/explore.html', {
        'experiences': experiences,
        'shops': shops,
        'dishes': dishes,
        'locations': locations,
    })

def dish_detail(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    reviews = Review.objects.filter(object_id=dish.pk).order_by('-created_at')
    return render(request, 'core/dish_detail.html', {'dish': dish, 'reviews': reviews})

def shop_detail(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    reviews = Review.objects.filter(object_id=shop.pk).order_by('-created_at')
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        if 'rating' in request.POST:
            if not request.user.is_tourist:
                messages.error(request, "Only tourists can leave a review.")
                return redirect('shop_detail', pk=pk)

            rating = request.POST.get('rating')
            comment = request.POST.get('comment')
            Review.objects.create(
                user=request.user,
                content_object=shop,
                rating=rating,
                comment=comment
            )
            return redirect('shop_detail', pk=pk)

        else:
            if not request.user.is_tourist:
                messages.error(request, "Only tourists can book a table.")
                return redirect('shop_detail', pk=pk)

            date = request.POST.get('date')
            guests = request.POST.get('guests')
            booking = Booking.objects.create(
                user=request.user,
                content_object=shop,
                date=date,
                guests=guests,
                status='confirmed'
            )
            return redirect('booking_confirmation', pk=booking.pk)

    return render(request, 'core/shop_detail.html', {
        'shop': shop,
        'reviews': reviews,
        'average_rating': average_rating
    })

def experience_detail(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    reviews = Review.objects.filter(object_id=experience.pk).order_by('-created_at')
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, object_id=experience.pk).exists()
    
    if request.method == 'POST' and 'rating' in request.POST:
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.is_vendor and experience.vendor.user == request.user:
            messages.error(request, "You cannot review your own experience.")
            return redirect('experience_detail', pk=pk)

        if not request.user.is_tourist:
            messages.error(request, "Only tourists can leave a review.")
            return redirect('experience_detail', pk=pk)
        
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        Review.objects.create(
            user=request.user,
            content_object=experience,
            rating=rating,
            comment=comment
        )
        return redirect('experience_detail', pk=pk)
        
    return render(request, 'core/experience_detail.html', {'experience': experience, 'reviews': reviews, 'is_favorite': is_favorite})

@login_required
def payment_page(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    if not request.user.is_tourist:
        messages.error(request, "Only tourists can book experiences.")
        return redirect('experience_detail', pk=pk)

    if request.method == 'POST':
        date = request.POST.get('date')
        guests = int(request.POST.get('guests'))
        total_price = experience.price * guests
        return render(request, 'core/payment.html', {
            'experience': experience,
            'date': date,
            'guests': guests,
            'total_price': total_price
        })
    return redirect('experience_detail', pk=pk)

@login_required
def process_payment(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    if request.method == 'POST':
        date = request.POST.get('date')
        guests = request.POST.get('guests')
        booking = Booking.objects.create(
            user=request.user,
            content_object=experience,
            date=date,
            guests=guests,
            status='confirmed'
        )
        return redirect('booking_confirmation', pk=booking.pk)
    return redirect('experience_detail', pk=pk)

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

    experience_content_type = ContentType.objects.get_for_model(Experience)
    favorite_experiences_ids = Favorite.objects.filter(
        user=request.user,
        content_type=experience_content_type
    ).values_list('object_id', flat=True)
    favorite_experiences = Experience.objects.filter(pk__in=favorite_experiences_ids)

    return render(request, 'core/profile.html', {
        'form': form,
        'bookings': bookings,
        'favorites': favorite_experiences,
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
    
    shop, created = Shop.objects.get_or_create(user=request.user, defaults={
        'business_name': f"{request.user.username}'s Business",
        'description': 'Please update your business description.',
        'location': 'Singapore',
        'contact_number': 'Unknown'
    })
    
    experiences = Experience.objects.filter(vendor=request.user.shop_profile)
    incoming_bookings = Booking.objects.filter(content_object__vendor=request.user.shop_profile).order_by('-date')
    
    return render(request, 'core/vendor_dashboard.html', {
        'experiences': experiences,
        'shop': request.user.shop_profile,
        'incoming_bookings': incoming_bookings
    })

@login_required
def add_listing(request):
    if not request.user.is_vendor:
        return redirect('home')
    
    shop = request.user.shop_profile
    
    if request.method == 'POST':
        form = ExperienceForm(request.POST, request.FILES)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.vendor = shop
            experience.save()
            return redirect('vendor_dashboard')
    else:
        form = ExperienceForm()
    return render(request, 'core/add_listing.html', {'form': form, 'title': 'Add New Experience'})

@login_required
def edit_listing(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    if request.user != experience.vendor.user:
        return redirect('home')
        
    if request.method == 'POST':
        form = ExperienceForm(request.POST, request.FILES, instance=experience)
        if form.is_valid():
            form.save()
            return redirect('vendor_dashboard')
    else:
        form = ExperienceForm(instance=experience)
    return render(request, 'core/add_listing.html', {'form': form, 'title': 'Edit Experience'})

@login_required
def delete_listing(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    if request.user == experience.vendor.user:
        experience.delete()
    return redirect('vendor_dashboard')

@login_required
def toggle_favorite(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    favorite, created = Favorite.objects.get_or_create(user=request.user, content_object=experience)
    if not created:
        favorite.delete()
    return redirect('experience_detail', pk=pk)

@login_required
def edit_vendor_profile(request):
    if not request.user.is_vendor:
        return redirect('home')
    
    shop = request.user.shop_profile
    
    if request.method == 'POST':
        form = ShopProfileForm(request.POST, request.FILES, instance=shop)
        if form.is_valid():
            form.save()
            return redirect('vendor_dashboard')
    else:
        form = ShopProfileForm(instance=shop)
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
    shop = get_object_or_404(Shop, pk=pk)
    experiences = Experience.objects.filter(vendor=shop)
    return render(request, 'core/vendor_detail.html', {'shop': shop, 'experiences': experiences})
