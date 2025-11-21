# TasteLocal - Local Food Tourism Platform

TasteLocal is a web-based platform designed to connect tourists with authentic local culinary experiences in Singapore. It empowers small-scale food vendors to showcase their offerings and allows tourists to discover, book, and review unique food spots.

## Features

### For Tourists
*   **Search & Discovery:** Filter experiences by Keyword, Location, Price, and Rating.
*   **Interactive Map:** View search results on an interactive map to find nearby food spots.
*   **Booking System:** Reserve tables or book food tours directly.
*   **Favorites:** Save interesting listings to your personal wishlist.
*   **Reviews:** Read and leave reviews for experiences.

### For Vendors
*   **Dashboard:** Manage listings, view incoming bookings, and update profile details.
*   **Profile Management:** Update business name, description, location, hours, and photos.
*   **Promotions:** Highlight special offers with discount pricing.

## Technology Stack
*   **Backend:** Django (Python)
*   **Frontend:** HTML, CSS, JavaScript (Leaflet.js for maps)
*   **Database:** SQLite (Default) / MySQL (Compatible)
*   **AI Integration:** Pollinations.ai API for image generation

## Prerequisites
*   Python 3.8 or higher
*   pip (Python package manager)

## Setup Instructions

### 1. Clone or Download the Repository
Ensure you have the project files in a directory on your local machine.

### 2. Create a Virtual Environment
It is recommended to run the project in a virtual environment.
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
Install the required Python packages.
```bash
pip install -r requirements.txt
```

### 4. Database Setup
Apply the database migrations to create the necessary tables.
```bash
python manage.py migrate
```

### 5. Create a Superuser (Optional)
Create an admin account to access the Django admin panel.
```bash
python manage.py createsuperuser
```

### 6. Populate Data (One-Time Setup)
Run the helper scripts to generate AI images and set vendor locations. You only need to do this once; the data will be saved to the database.
```bash
# Generate images for listings and vendors
python generate_images.py

# Populate real coordinates for map view
python update_coordinates.py
```

### 7. Run the Development Server
Start the local server.
```bash
python manage.py runserver
```

### 8. Access the Application
Open your web browser and go to:
`http://127.0.0.1:8000/`

## Usage Guide

### Vendor Workflow
1.  **Sign Up:** Create a new account and select "I am a Vendor".
2.  **Dashboard:** You will be redirected to the Vendor Dashboard.
3.  **Edit Profile:** Click "Edit Profile" to set your business name, description, hours, and location.
4.  **Add Listing:** Click "Add New Listing" to create a food experience.
5.  **Manage Bookings:** View and manage incoming bookings on your dashboard.

### Tourist Workflow
1.  **Sign Up/Login:** Create an account (default is Tourist).
2.  **Browse:** Use the "Experiences" page to search for food.
3.  **Filter:** Use the filter bar or "Show Map View" to find specific spots.
4.  **Book:** Click on a listing and use the booking form.
5.  **Review:** After your visit, leave a review on the listing page.

## Project Structure
*   `core/`: Main Django app containing models, views, and forms.
*   `templates/`: HTML templates for the application.
*   `static/`: CSS, JavaScript, and image assets.
*   `docs/`: Project documentation and requirements.
