#
# This file (`core/views.py`) contains the business logic for the TasteLocal application.
# A view function in Django takes a web request and returns a web response.
#
# These views are responsible for:
# - Handling user input from forms (`core/forms.py`).
# - Interacting with the database via models (`core/models.py`).
# - Rendering HTML templates (`templates/` and `core/templates/`) with context data.
# - Handling user authentication and authorization.
# - Processing API requests and returning JSON data.
#
# Each view function is mapped to a specific URL pattern in `core/urls.py`.
#
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
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

# Import all custom forms used in the views.
from .forms import (
    CustomUserCreationForm,
    ExperienceForm,
    ShopProfileForm,
    UserProfileForm,
    BookingForm,
    TouristUserEditForm,
    TouristProfileEditForm,
    ReviewForm,
    DishForm,
)

#
# Handles the creation of a new Dish by a vendor.
# This view is protected, requiring the user to be logged in and a vendor.
#
@login_required
def add_dish(request):
    # Authorization check: only vendors can add dishes.
    if not request.user.is_vendor:
        return redirect('home')

    # Get the vendor's shop profile.
    shop = request.user.shop_profile

    # Handle form submission.
    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a Dish object but don't save to the database yet.
            dish = form.save(commit=False)
            # Associate the dish with the vendor's shop.
            dish.shop = shop
            # Now save the dish to the database.
            dish.save()
            # Redirect to the vendor dashboard on success.
            return redirect('vendor_dashboard')
    # Handle initial GET request (show an empty form).
    else:
        form = DishForm()
    # Render the form template.
    return render(request, 'core/add_dish.html', {'form': form, 'title': 'Add New Dish'})

#
# Handles the editing of an existing Dish by its owner.
#
@login_required
def edit_dish(request, pk):
    # Retrieve the dish or return a 404 error if not found.
    dish = get_object_or_404(Dish, pk=pk)
    # Authorization check: only the shop owner can edit the dish.
    if request.user != dish.shop.user:
        return redirect('home')

    # Handle form submission with the existing dish instance.
    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES, instance=dish)
        if form.is_valid():
            form.save()
            return redirect('vendor_dashboard')
    # Handle initial GET request (show the form pre-filled with dish data).
    else:
        form = DishForm(instance=dish)
    # Render the form template.
    return render(request, 'core/add_dish.html', {'form': form, 'title': 'Edit Dish'})

#
# Handles the deletion of a Dish by its owner.
#
@login_required
def delete_dish(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    # Authorization check.
    if request.user == dish.shop.user:
        dish.delete()
    # Redirect back to the dashboard.
    return redirect('vendor_dashboard')

#
# Renders the home page.
#
def home(request):
    # Query the database for featured content to display on the home page.
    featured_experiences = Experience.objects.all().order_by('-created_at')[:3]
    all_shops = Shop.objects.all()
    featured_dishes = Dish.objects.order_by('?')[:4]
    # Render the home page template with the queried data.
    return render(request, 'home.html', {
        'featured_experiences': featured_experiences,
        'all_shops': all_shops,
        'featured_dishes': featured_dishes
    })

#
# Renders the static 'About' page.
#
def about(request):
    return render(request, 'about.html')

#
# Renders the main 'Explore' page and handles search and filtering logic.
#
def explore(request):
    # Get filter parameters from the GET request.
    query = request.GET.get('q')
    location = request.GET.get('location')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    min_rating = request.GET.get('min_rating')
    active_tab = request.GET.get('active_tab', 'dishes') # Default to 'dishes' tab.

    # Start with all objects for each model.
    experiences = Experience.objects.all()
    shops = Shop.objects.all()
    dishes = Dish.objects.all()

    # Apply keyword search filter if provided.
    if query:
        # Use Q objects for complex queries (OR conditions).
        experiences = experiences.filter(Q(title__icontains=query) | Q(description__icontains=query))
        shops = shops.filter(Q(business_name__icontains=query) | Q(description__icontains=query))
        dishes = dishes.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # Apply location filter.
    if location:
        # Filter related models using the '__' syntax.
        experiences = experiences.filter(vendor__location__icontains=location)
        shops = shops.filter(location__icontains=location)
        dishes = dishes.filter(shop__location__icontains=location)

    # Apply price filters.
    if min_price:
        experiences = experiences.filter(price__gte=min_price)
        dishes = dishes.filter(price__gte=min_price)
    if max_price:
        experiences = experiences.filter(price__lte=max_price)
        dishes = dishes.filter(price__lte=max_price)

    # Apply minimum rating filter.
    if min_rating:
        # Annotate the queryset with the average rating, then filter on it.
        experiences = experiences.annotate(avg_rating=Avg('review__rating')).filter(avg_rating__gte=min_rating)
        shops = shops.annotate(avg_rating=Avg('review__rating')).filter(avg_rating__gte=min_rating)
        dishes = dishes.annotate(avg_rating=Avg('review__rating')).filter(avg_rating__gte=min_rating)
        
    # Get a distinct list of all shop locations for the filter dropdown.
    locations = Shop.objects.values_list('location', flat=True).distinct()

    # Get a list of IDs for all items the current user has favorited.
    # This is used to show the correct state of the 'favorite' button in the template.
    favorite_shops_ids = []
    favorite_dishes_ids = []
    favorite_experiences_ids = []
    if request.user.is_authenticated and request.user.is_tourist:
        favorite_shops_ids = Favorite.objects.filter(user=request.user, content_type=ContentType.objects.get_for_model(Shop)).values_list('object_id', flat=True)
        favorite_dishes_ids = Favorite.objects.filter(user=request.user, content_type=ContentType.objects.get_for_model(Dish)).values_list('object_id', flat=True)
        favorite_experiences_ids = Favorite.objects.filter(user=request.user, content_type=ContentType.objects.get_for_model(Experience)).values_list('object_id', flat=True)

    # Prepare the context and render the template.
    return render(request, 'core/explore.html', {
        'experiences': experiences,
        'shops': shops,
        'dishes': dishes,
        'locations': locations,
        'favorite_shops_ids': list(favorite_shops_ids),
        'favorite_dishes_ids': list(favorite_dishes_ids),
        'favorite_experiences_ids': list(favorite_experiences_ids),
        'active_tab': active_tab,
    })

#
# Renders the detail page for a single Dish and handles review submission.
#
def dish_detail(request, pk):
    dish = get_object_or_404(Dish, pk=pk)

    # Use ContentType framework to fetch reviews for this specific dish.
    dish_content_type = ContentType.objects.get_for_model(Dish)
    reviews = Review.objects.filter(content_type=dish_content_type, object_id=dish.pk).order_by('-created_at')

    # Calculate the average rating.
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    # Initialize the review form.
    review_form = ReviewForm()

    # Check if the current user has favorited this dish.
    is_favorite = False
    if request.user.is_authenticated and request.user.is_tourist:
        is_favorite = Favorite.objects.filter(user=request.user, content_type=ContentType.objects.get_for_model(Dish), object_id=dish.pk).exists()

    # Handle review form submission.
    if request.method == 'POST':
        # Authentication and authorization checks.
        if not request.user.is_authenticated:
            return redirect('login')
        if not request.user.is_tourist:
            messages.error(request, "Only tourists can leave a review.")
            return redirect('dish_detail', pk=pk)

        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            # Link the review to the dish using the generic foreign key.
            review.content_object = dish
            review.save()
            # Redirect to the same page to show the new review.
            return redirect('dish_detail', pk=pk)

    # Prepare context and render the template.
    return render(request, 'core/dish_detail.html', {
        'dish': dish,
        'reviews': reviews,
        'average_rating': average_rating,
        'review_form': review_form,
        'is_favorite': is_favorite
    })

#
# Renders the detail page for a single Shop and handles both review and booking submissions.
#
def shop_detail(request, pk):
    shop = get_object_or_404(Shop, pk=pk)

    # Fetch reviews and calculate average rating for the shop.
    shop_content_type = ContentType.objects.get_for_model(Shop)
    reviews = Review.objects.filter(content_type=shop_content_type, object_id=shop.pk).order_by('-created_at')
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    # Initialize forms.
    booking_form = BookingForm(shop=shop) # Pass shop for validation.
    review_form = ReviewForm()

    # Check if the shop is favorited by the user.
    is_favorite = False
    if request.user.is_authenticated and request.user.is_tourist:
        is_favorite = Favorite.objects.filter(user=request.user, content_type=ContentType.objects.get_for_model(Shop), object_id=shop.pk).exists()

    # Handle POST requests (could be a review or a booking).
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        # Differentiate between review and booking forms by checking for a 'rating' field.
        if 'rating' in request.POST: # This is a review submission.
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.user = request.user
                review.content_object = shop
                review.save()
                return redirect('shop_detail', pk=pk)

        else: # This is a booking submission.
            if not request.user.is_tourist:
                messages.error(request, "Only tourists can book a table.")
                return redirect('shop_detail', pk=pk)

            booking_form = BookingForm(request.POST, shop=shop)
            if booking_form.is_valid():
                booking = booking_form.save(commit=False)
                booking.user = request.user
                booking.content_object = shop
                booking.status = 'confirmed' # Auto-confirm table bookings.
                booking.save()
                return redirect('booking_confirmation', pk=booking.pk)
            else:
                # If booking form is invalid, re-render the page with the form errors.
                is_favorite = Favorite.objects.filter(user=request.user, content_type=ContentType.objects.get_for_model(Shop), object_id=shop.pk).exists()
                return render(request, 'core/shop_detail.html', {
                    'shop': shop,
                    'reviews': reviews,
                    'average_rating': average_rating,
                    'booking_form': booking_form, # Pass the invalid form back.
                    'is_favorite': is_favorite,
                    'opening_hours_json': shop.opening_hours_structured
                })

    # Handle GET request.
    return render(request, 'core/shop_detail.html', {
        'shop': shop,
        'reviews': reviews,
        'average_rating': average_rating,
        'booking_form': booking_form,
        'review_form': review_form,
        'is_favorite': is_favorite,
        'opening_hours_json': shop.opening_hours_structured
    })

#
# Renders the detail page for a single Experience and handles review submission.
#
def experience_detail(request, pk):
    experience = get_object_or_404(Experience, pk=pk)

    # Fetch reviews and calculate average rating.
    experience_content_type = ContentType.objects.get_for_model(Experience)
    reviews = Review.objects.filter(content_type=experience_content_type, object_id=experience.pk).order_by('-created_at')
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    review_form = ReviewForm()

    # Check if favorited.
    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user=request.user, content_type=experience_content_type, object_id=experience.pk).exists()
    
    # Handle review submission.
    if request.method == 'POST' and 'rating' in request.POST:
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.content_object = experience
            review.save()
            return redirect('experience_detail', pk=pk)
        
    # Render the template.
    return render(request, 'core/experience_detail.html', {'experience': experience, 'reviews': reviews, 'review_form': review_form, 'is_favorite': is_favorite})

#
# Renders the payment summary page for an Experience booking.
#
@login_required
def payment_page(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    # Authorization check.
    if not request.user.is_tourist:
        messages.error(request, "Only tourists can book experiences.")
        return redirect('experience_detail', pk=pk)

    # This view is reached after a user submits booking details on the experience page.
    if request.method == 'POST':
        # Get booking details from the POST request.
        date = request.POST.get('date')
        time = request.POST.get('time')
        guests = int(request.POST.get('guests'))
        # Calculate the total price.
        total_price = experience.price * guests
        # Render the payment summary page.
        return render(request, 'core/payment.html', {
            'experience': experience,
            'date': date,
            'time': time,
            'guests': guests,
            'total_price': total_price
        })
    # Redirect if accessed directly via GET.
    return render(request, 'core/payment.html', {'experience': experience})

#
# Processes the "payment" (creates the booking record) after user confirmation.
#
@login_required
def process_payment(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    if request.method == 'POST':
        # Get booking details again from the hidden form fields on the payment page.
        date = request.POST.get('date')
        guests = request.POST.get('guests')
        # Create the Booking object in the database.
        booking = Booking.objects.create(
            user=request.user,
            content_object=experience,
            date=date,
            guests=guests,
            status='confirmed' # Bookings for experiences are confirmed upon payment.
        )
        # Redirect to the confirmation page.
        return redirect('booking_confirmation', pk=booking.pk)
    # Redirect if accessed directly via GET.
    return redirect('experience_detail', pk=pk)

#
# Displays the final booking confirmation page to the user.
#
@login_required
def booking_confirmation(request, pk):
    # Fetch the booking, ensuring it belongs to the current user for security.
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'core/booking_confirmation.html', {'booking': booking})

#
# Allows a user to cancel one of their own bookings.
#
@login_required
def cancel_booking(request, pk):
    # Fetch the booking, ensuring it belongs to the current user.
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    # Check if the booking is not already cancelled.
    if booking.status != 'cancelled':
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Your booking has been cancelled.')
    else:
        messages.error(request, 'This booking has already been cancelled.')
    # Redirect back to the user's profile page.
    return redirect('profile')

#
# Renders the user's profile page, showing their bookings and favorites.
#
@login_required
def profile(request):
    # Get or create a UserProfile for the current user.
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    form = UserProfileForm(instance=user_profile)

    # Fetch all bookings for the current user, ordered by date.
    bookings = Booking.objects.filter(user=request.user).order_by('-date')

    # Get ContentType instances for our models to query generic relations.
    shop_content_type = ContentType.objects.get_for_model(Shop)
    dish_content_type = ContentType.objects.get_for_model(Dish)
    experience_content_type = ContentType.objects.get_for_model(Experience)

    # Fetch IDs of all favorited items for the user.
    favorite_shops_ids = Favorite.objects.filter(user=request.user, content_type=shop_content_type).values_list('object_id', flat=True)
    favorite_dishes_ids = Favorite.objects.filter(user=request.user, content_type=dish_content_type).values_list('object_id', flat=True)
    favorite_experiences_ids = Favorite.objects.filter(user=request.user, content_type=experience_content_type).values_list('object_id', flat=True)

    # Fetch the actual favorited objects using the retrieved IDs.
    favorite_shops = Shop.objects.filter(pk__in=favorite_shops_ids)
    favorite_dishes = Dish.objects.filter(pk__in=favorite_dishes_ids)
    favorite_experiences = Experience.objects.filter(pk__in=favorite_experiences_ids)

    # Render the profile template with all the fetched data.
    return render(request, 'core/profile.html', {
        'form': form,
        'bookings': bookings,
        'favorite_shops': favorite_shops,
        'favorite_dishes': favorite_dishes,
        'favorite_experiences': favorite_experiences,
        'user_profile': user_profile
    })

#
# Handles user registration.
#
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Save the new user to the database.
            user = form.save()
            # Log the user in immediately.
            login(request, user)

            # Send a welcome email to the new user.
            subject = 'Welcome to TasteLocal!'
            # Render the email content from an HTML template.
            html_message = render_to_string('registration/welcome_email.html', {'user': user})
            # Create a plain text version for email clients that don't support HTML.
            plain_message = strip_tags(html_message)
            from_email = settings.EMAIL_HOST_USER
            to = user.email

            # Send the email.
            send_mail(subject, plain_message, from_email, [to], html_message=html_message)

            # Redirect based on the user's chosen role.
            if user.is_vendor:
                return redirect('vendor_dashboard')
            else:
                return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

#
# Renders the dashboard for vendor users.
#
@login_required
def vendor_dashboard(request):
    # Authorization check.
    if not request.user.is_vendor:
        return redirect('home')
    
    # Get or create the vendor's shop profile. If a new vendor registers,
    # a default shop profile is created for them.
    shop, created = Shop.objects.get_or_create(user=request.user, defaults={
        'business_name': f"{request.user.username}'s Business",
        'description': 'Please update your business description.',
        'location': 'Singapore',
        'contact_number': 'Unknown'
    })
    
    # Fetch all experiences and dishes associated with the vendor's shop.
    experiences = Experience.objects.filter(vendor=request.user.shop_profile)
    dishes = Dish.objects.filter(shop=request.user.shop_profile)

    # Fetch all incoming bookings for the vendor's shop and any of their experiences.
    shop_type = ContentType.objects.get_for_model(Shop)
    experience_type = ContentType.objects.get_for_model(Experience)
    experience_ids = experiences.values_list('pk', flat=True)

    # A complex query to get bookings related to either the shop OR any of its experiences.
    incoming_bookings = Booking.objects.filter(
        (Q(content_type=shop_type) & Q(object_id=shop.pk)) |
        (Q(content_type=experience_type) & Q(object_id__in=experience_ids))
    ).order_by('-date')
    
    # Render the dashboard template.
    return render(request, 'core/vendor_dashboard.html', {
        'experiences': experiences,
        'dishes': dishes,
        'shop': request.user.shop_profile,
        'incoming_bookings': incoming_bookings
    })

#
# Handles the creation of a new Experience listing by a vendor.
#
@login_required
def add_listing(request):
    # Authorization check.
    if not request.user.is_vendor:
        return redirect('home')
    
    # Get the vendor's shop to associate with the new experience.
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

#
# Handles the editing of an existing Experience listing.
#
@login_required
def edit_listing(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    # Authorization check: only the owner can edit.
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

#
# Handles the deletion of an Experience listing.
#
@login_required
def delete_listing(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    # Authorization check.
    if request.user == experience.vendor.user:
        experience.delete()
    return redirect('vendor_dashboard')

#
# A legacy view for toggling favorites.
# NOTE: This is no longer used by the frontend, which now uses the API endpoint.
#
@login_required
def toggle_favorite(request, pk):
    experience = get_object_or_404(Experience, pk=pk)
    # get_or_create returns the object and a boolean indicating if it was created.
    favorite, created = Favorite.objects.get_or_create(user=request.user, content_object=experience)
    # If the favorite already existed, delete it.
    if not created:
        favorite.delete()
    return redirect('experience_detail', pk=pk)

#
# Handles the editing of a vendor's own shop profile.
#
@login_required
def edit_vendor_profile(request):
    # Authorization check.
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

#
# A custom LoginView to redirect users based on their role after login.
# Inherits from Django's built-in LoginView.
#
class CustomLoginView(LoginView):
    # Overrides the default success URL.
    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            # Vendors go to their dashboard, tourists go to their profile.
            if user.is_vendor:
                return reverse_lazy('vendor_dashboard')
            else:
                return reverse_lazy('profile')
        return reverse_lazy('login')

#
# Renders the public detail page for a vendor's shop.
#
def vendor_detail(request, pk):
    shop = get_object_or_404(Shop, pk=pk)
    # Fetch all experiences offered by this shop.
    experiences = Experience.objects.filter(vendor=shop)
    return render(request, 'core/vendor_detail.html', {'shop': shop, 'experiences': experiences})

#
# Handles the editing of a tourist's user and profile information.
#
@login_required
def profile_edit_view(request):
    # Authorization check.
    if not request.user.is_tourist:
        return redirect('home')

    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Use two separate forms for editing the User and UserProfile models.
        user_form = TouristUserEditForm(request.POST, instance=request.user)
        profile_form = TouristProfileEditForm(request.POST, request.FILES, instance=user_profile)

        # Both forms must be valid to proceed.
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        user_form = TouristUserEditForm(instance=request.user)
        profile_form = TouristProfileEditForm(instance=user_profile)

    return render(request, 'core/edit_tourist_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

#
# API endpoint to toggle an item's favorite status.
# This view is designed to be called by JavaScript (fetch) and returns JSON.
#
@require_POST  # Ensures this view only accepts POST requests.
@login_required
def toggle_favorite_api(request, model_name, pk):
    # Authorization check.
    if not request.user.is_tourist:
        return JsonResponse({'status': 'error', 'message': 'Only tourists can favorite items.'}, status=403)

    try:
        # Map the model name from the URL to the actual model class.
        model_map = {'shop': Shop, 'dish': Dish, 'experience': Experience}
        model = model_map.get(model_name.lower())
        if not model:
            return JsonResponse({'status': 'error', 'message': 'Invalid item type.'}, status=400)

        # Use ContentType to work with the generic relationship.
        content_type = ContentType.objects.get_for_model(model)
        favorite, created = Favorite.objects.get_or_create(user=request.user, content_type=content_type, object_id=pk)

        # If the favorite was newly created, it means we added it.
        if created:
            return JsonResponse({'status': 'added', 'message': 'Added to favorites.'})
        # If it already existed, we delete it.
        else:
            favorite.delete()
            return JsonResponse({'status': 'removed', 'message': 'Removed from favorites.'})
    # Catch any potential errors and return a generic server error response.
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
