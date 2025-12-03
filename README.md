# TasteLocal - Local Food Tourism Platform

TasteLocal is a web-based platform designed to connect tourists with authentic local culinary experiences in Singapore. It empowers small-scale food vendors to showcase their offerings and allows tourists to discover, book, and review unique food spots.

## Features

### For Tourists
*   **Search & Discovery:** Filter dishes, shops, and experiences by Keyword, Location, Price, and Rating.
*   **Interactive Map:** View search results on an interactive map to find nearby food spots.
*   **Booking System:** Reserve tables or book food tours directly.
*   **Favorites:** Save interesting dishes, shops, and experiences to your personal "Food Trail".
*   **Reviews:** Read and leave reviews for experiences.
*   **Profile Editing:** Update your username, email, and contact information.

### For Vendors
*   **Dashboard:** Manage listings, view incoming bookings, and update profile details.
*   **Profile Management:** Update business name, description, location, hours, and photos.

## Technology Stack
*   **Backend:** Django (Python)
*   **Frontend:** HTML, CSS, JavaScript (Leaflet.js for maps)
*   **Database:** MySQL
*   **AI Integration:** Pollinations.ai API for image generation

## Prerequisites
*   Python 3.8 or higher
*   pip (Python package manager)
*   MySQL

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
This project is configured to use a MySQL database.

**a. Install and Start MySQL:**
Follow the official instructions for your operating system to install and start the MySQL server.

**b. Create the Database:**
Connect to MySQL and create a new database for the project.
```sql
CREATE DATABASE tastelocal;
```

**c. Configure Environment Variables:**
The Django settings are configured to read database credentials from environment variables. Create a `.env` file in the project's root directory and add the following, replacing the placeholder values with your actual database credentials:

```
DB_NAME=tastelocal
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_HOST=127.0.0.1
DB_PORT=3306
SECRET_KEY=your-secret-key
```
**Note:** The `SECRET_KEY` is a Django-specific value for cryptographic signing and should be a long, random string.

### 5. Apply Migrations
Apply the database migrations to create the necessary tables.
```bash
python manage.py migrate
```

### 6. Create a Superuser (Optional)
Create an admin account to access the Django admin panel.
```bash
python manage.py createsuperuser
```

### 7. Populate Data with Singaporean Food Scene
Run the `populate_singapore_data.py` script to fill the database with 30 real food stalls from Singapore's hawker centres, each with 5 dishes. This script will also generate AI images for all entries.

**Note:** This process can take several minutes as it fetches and saves over 150 images.
```bash
python populate_singapore_data.py
```

### 8. Run the Development Server
Start the local server.
```bash
python manage.py runserver
```

### 9. Access the Application
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
2.  **Browse:** Use the "Explore" page to search for food, shops, and experiences.
3.  **Filter:** Use the filter bar or "Show Map View" to find specific spots.
4.  **Book:** Click on a listing and use the booking form.
5.  **Review:** After your visit, leave a review on the listing page.
6.  **Favorites:** Click the "Heart" icon on any listing to add it to your "My Favorites" page.

## Project Structure
*   `core/`: Main Django app containing models, views, and forms.
*   `templates/`: HTML templates for the application.
*   `static/`: CSS, JavaScript, and image assets.
*   `docs/`: Project documentation and requirements.
