# Task 6: Testing & Evaluation Guide

This document provides a structured guide to testing the **TasteLocal** platform. It includes test accounts and step-by-step instructions to verify that all project requirements have been met.

## 1. Test Accounts

Use the following credentials to log in and test the application.

| Role | Username | Password | Purpose |
| :--- | :--- | :--- | :--- |
| **Tourist** | `tourist_john` | `TestPass123!` | Test search, booking, and reviews. |
| **Vendor** | `vendor_tina` | `TestPass123!` | Test profile management, listing creation, and booking management. |
| **Admin** | `admin` | `TestPass123!` | Access Django Admin panel (if needed). |

---

## 2. Tourist Workflow Testing
**Objective:** Verify that a tourist can discover, book, and review experiences.

### Step 1: Search & Discovery
1.  Log in as `tourist_john`.
2.  Navigate to the **"Experiences"** page.
3.  **Keyword Search:** Enter "Chicken" in the search bar and click "Apply Filters". Verify that "Traditional Chicken Rice Workshop" appears.
4.  **Location Filter:** Select "Chinatown" from the location dropdown. Verify results update.
5.  **Map View:** Click **"Show Map View"**. Verify that a map appears with pins. Click a pin to see the popup.
6.  **Price Filter:** Set Max Price to $50. Verify that expensive listings disappear.

### Step 2: Booking an Experience
1.  Click on "Traditional Chicken Rice Workshop" (or any listing).
2.  **View Details:** Check if the description, price, and map are visible.
3.  **Book:** Fill in the "Book This Experience" form:
    *   **Date:** Select a future date.
    *   **Guests:** Enter `2`.
    *   Click **"Proceed to Payment"**.
4.  **Payment:** You will see a payment confirmation screen. Click **"Confirm Payment"**.
5.  **Confirmation:** You should be redirected to your Profile page showing the new booking with status "Confirmed".

### Step 3: Favorites & Reviews
1.  Go back to the "Experiences" page.
2.  **Favorite:** Click the "Heart" icon (or "Save to Favorites" button) on a listing.
3.  Go to **"Profile"** -> **"My Favorites"**. Verify the listing is there.
4.  **Review:** (Note: You can usually only review after a booking, but for testing, check if the review form exists on the Listing Detail page). Leave a 5-star rating and a comment. Verify it appears at the bottom of the page.

---

## 3. Vendor Workflow Testing
**Objective:** Verify that a vendor can manage their business presence.

### Step 1: Profile Management
1.  Log out and log in as `vendor_tina`.
2.  You should be redirected to the **Vendor Dashboard**.
3.  **Edit Profile:** Click the "Edit Profile" button.
    *   Change "Business Name" to "Tina's Super Kitchen".
    *   Update "Opening Hours" to "Daily: 9am - 9pm".
    *   Click **"Save Changes"**.
4.  Verify the dashboard now shows the updated details.

### Step 2: Manage Listings
1.  **Add Listing:** Click **"Add New Listing"**.
    *   **Title:** "Spicy Laksa Challenge".
    *   **Description:** "Can you handle the heat?".
    *   **Price:** `15.00`.
    *   **Image:** (Optional, or upload a sample).
    *   Click **"Create Listing"**.
2.  **Verify:** Check that the new listing appears in the "My Listings" section of the dashboard.
3.  **Edit Listing:** Click "Edit" on the new listing. Change the price to `18.00` and save.

### Step 3: Manage Bookings
1.  Look at the **"Incoming Bookings"** section on the dashboard.
2.  You should see the booking made by `tourist_john` in the previous test.
3.  Verify it shows the correct Date, Guests, and Status.

---

## 4. Requirement Verification Checklist

| Requirement | Feature Implemented | Test Status |
| :--- | :--- | :--- |
| **Search & Discovery** | Keyword, Location, Price, Rating filters | [ ] Pass |
| **Geolocation** | Interactive Map View with Pins | [ ] Pass |
| **Booking System** | Booking form + Simulated Payment | [ ] Pass |
| **Itinerary/Favorites** | "Save to Favorites" functionality | [ ] Pass |
| **Vendor Profile** | Edit Profile (Name, Hours, Location, Photo) | [ ] Pass |
| **Promotions** | Discount Price field (strikethrough display) | [ ] Pass |
| **Reviews** | User ratings and comments | [ ] Pass |

## 5. Resetting Data (Optional)
If you need to wipe the database and start over:
1.  Delete `db.sqlite3`.
2.  Run `python manage.py migrate`.
3.  Run `python create_test_users.py`.
4.  Run `python generate_images.py` and `python update_coordinates.py`.
