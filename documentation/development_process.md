# Development Process

This document outlines the step-by-step process that was followed to build the TasteLocal web application.

## 1. Project Initialization and Setup

*   **Django Project Creation:** The project was initiated by creating a new Django project and a core application to house the main functionality.
*   **Database Configuration:** The project was configured to use MySQL as the database, and the necessary settings were added to `TasteLocal/settings.py`.
*   **Virtual Environment:** A virtual environment was set up to manage project dependencies, and the required packages were installed from `requirements.txt`.

## 2. Data Modeling

*   **Model Definition:** The database models were defined in `core/models.py`. This involved creating classes for `User`, `UserProfile`, `Dish`, `Shop`, `Experience`, `Booking`, `Review`, and `Favorite`.
*   **Relationships:** The relationships between the models were established using Django's ORM, including one-to-one, one-to-many, many-to-many, and generic relationships.
*   **Migrations:** Database migrations were created and applied to translate the models into database tables.

## 3. User Authentication and Profiles

*   **Custom User Model:** The default Django `User` model was extended to include user roles (`is_tourist`, `is_vendor`).
*   **Registration and Login:** User registration and login functionality was implemented, including custom forms and views.
*   **Profile Management:** Views and templates were created for users to view and edit their profiles.

## 4. Core Functionality

*   **Explore Page:** The main "Explore" page was developed to allow users to search and filter dishes, shops, and experiences.
*   **Detail Pages:** Detail pages were created for each of the core models (`Dish`, `Shop`, `Experience`) to display their information.
*   **Booking System:** A booking system was implemented to allow tourists to book experiences and reserve tables at shops.
*   **Review System:** A review system was added to allow tourists to leave reviews and ratings for dishes, shops, and experiences.
*   **Favorites:** A "favorites" feature was implemented to allow users to save items they are interested in.

## 5. Vendor Dashboard

*   **Dashboard Creation:** A dedicated dashboard was created for vendors to manage their business profiles, dishes, and experiences.
*   **CRUD Functionality:** The dashboard was equipped with functionality to create, read, update, and delete dishes and experiences.
*   **Booking Management:** A section was added to the dashboard for vendors to view and manage incoming bookings.

## 6. Frontend Development

*   **Templating:** HTML templates were created using Django's templating language to render the application's pages.
*   **Styling:** CSS was used to style the application and create a consistent look and feel.
*   **JavaScript:** JavaScript was used to add interactivity to the application, such as the interactive map on the "Explore" page and the asynchronous "favorites" feature.

## 7. Data Population

*   **Data Scripts:** Standalone Python scripts were written to populate the database with realistic data for development and testing.
*   **Image Generation:** An AI image generation service was integrated to create and download images for the populated data.

## 8. Testing and Debugging

*   **Testing:** A testing strategy was developed to ensure the application's functionality was working as expected.
*   **Debugging:** The application was thoroughly debugged to identify and fix any issues before deployment.

This step-by-step process ensured that the TasteLocal application was developed in a structured and organized manner, resulting in a robust and functional platform.
