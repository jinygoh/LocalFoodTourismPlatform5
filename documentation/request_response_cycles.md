# Request-Response Cycles

This document breaks down 10 key request-response cycles in the TasteLocal application. Each cycle follows the path from a user's action in their browser to the server's response.

---

### 1. Viewing the Home Page

*   **Request:**
    *   **Action:** User navigates to the root URL (`/`).
    *   **Method:** `GET`
    *   **URL:** `/`
    *   **Handler:** The request is routed by `TasteLocal/urls.py` to `core/urls.py`, which maps it to the `home` view in `core/views.py`.

*   **Response:**
    *   **View Logic:** The `home` view queries the database for featured experiences, shops, and dishes.
    *   **Template:** It renders the `home.html` template, passing the queried data as context.
    *   **Result:** The server sends back the rendered HTML, which the browser displays as the home page.

---

### 2. User Registration

*   **Request:**
    *   **Action:** User fills out the registration form and clicks "Sign Up".
    *   **Method:** `POST`
    *   **URL:** `/register/`
    *   **Handler:** `core/urls.py` maps this to the `register` view.

*   **Response:**
    *   **View Logic:** The `register` view processes the `POST` data using the `CustomUserCreationForm`. If the form is valid, a new `User` is created, the user is logged in, and a welcome email is sent.
    *   **Redirect:** The user is redirected to their profile page (`/profile/`) or the vendor dashboard (`/vendor/dashboard/`) depending on their selected role.
    *   **Result:** The browser receives the redirect and loads the new page.

---

### 3. Filtering on the Explore Page

*   **Request:**
    *   **Action:** User enters "Chicken Rice" in the search bar and clicks "Filter".
    *   **Method:** `GET`
    *   **URL:** `/explore/?q=Chicken+Rice`
    *   **Handler:** Mapped to the `explore` view.

*   **Response:**
    *   **View Logic:** The `explore` view retrieves the `q` parameter from the URL. It then filters the `Dish`, `Shop`, and `Experience` models based on this query.
    *   **Template:** It re-renders the `core/explore.html` template, but this time the context contains only the filtered results.
    *   **Result:** The server sends the updated HTML, and the user sees a list of items related to "Chicken Rice".

---

### 4. Viewing a Dish Detail Page

*   **Request:**
    *   **Action:** User clicks on a dish named "Hainanese Chicken Rice".
    *   **Method:** `GET`
    *   **URL:** `/dishes/5/` (where 5 is the dish's ID)
    *   **Handler:** Mapped to the `dish_detail` view.

*   **Response:**
    *   **View Logic:** The `dish_detail` view fetches the `Dish` with `pk=5` from the database, along with its associated reviews.
    *   **Template:** It renders the `core/dish_detail.html` template, passing the dish and its reviews in the context.
    *   **Result:** The user sees a detailed page for Hainanese Chicken Rice.

---

### 5. Adding an Item to Favorites (API Call)

*   **Request:**
    *   **Action:** User clicks the "heart" icon next to a shop.
    *   **Method:** `POST` (triggered by a JavaScript `fetch` call)
    *   **URL:** `/api/toggle_favorite/shop/12/` (where 12 is the shop's ID)
    *   **Handler:** Mapped to the `toggle_favorite_api` view.

*   **Response:**
    *   **View Logic:** The view identifies the user and the shop. It checks if a `Favorite` object exists for this combination. If not, it creates one. If it does, it deletes it.
    *   **JSON Response:** The view does not render a template. Instead, it returns a JSON object, e.g., `{"status": "added"}`.
    *   **Result:** The JavaScript on the page receives this JSON and updates the heart icon's color to red, providing instant feedback without a page reload.

---

### 6. Submitting a Review

*   **Request:**
    *   **Action:** User writes a review on a shop's detail page and clicks "Submit".
    *   **Method:** `POST`
    *   **URL:** `/shops/12/`
    *   **Handler:** Mapped to the `shop_detail` view.

*   **Response:**
    *   **View Logic:** The `shop_detail` view detects that the request is a `POST` and contains review data. It validates the data using the `ReviewForm`. If valid, it creates a new `Review` object linked to the current shop.
    *   **Redirect:** It then redirects the user back to the same `shop_detail` page.
    *   **Result:** The browser reloads the page, and the user's new review is now visible at the top of the reviews section.

---

### 7. Vendor Adding a New Experience

*   **Request:**
    *   **Action:** A vendor fills out the "Add New Experience" form and clicks "Save".
    *   **Method:** `POST`
    *   **URL:** `/shop/experiences/add/`
    *   **Handler:** Mapped to the `add_listing` view.

*   **Response:**
    *   **View Logic:** The `add_listing` view validates the submitted data with the `ExperienceForm`. If valid, it creates a new `Experience` object, associating it with the logged-in vendor's shop profile.
    *   **Redirect:** It redirects the vendor to their dashboard (`/vendor/dashboard/`).
    *   **Result:** The vendor is taken back to their dashboard and can see the newly created experience in their list of offerings.

---

### 8. Vendor Editing Their Profile

*   **Request:**
    *   **Action:** A vendor updates their business name and clicks "Update Profile".
    *   **Method:** `POST`
    *   **URL:** `/shop/profile/edit/`
    *   **Handler:** Mapped to the `edit_vendor_profile` view.

*   **Response:**
    *   **View Logic:** The view binds the incoming `POST` data to a `ShopProfileForm` instance for the vendor's existing shop. After validation, it saves the changes to the database.
    *   **Redirect:** It redirects the vendor to their dashboard.
    *   **Result:** The vendor sees their dashboard, and their updated business name is now displayed.

---

### 9. Tourist Cancelling a Booking

*   **Request:**
    *   **Action:** A tourist clicks the "Cancel" button next to a booking on their profile page.
    *   **Method:** `GET` (or could be `POST` for safety)
    *   **URL:** `/booking/cancel/8/` (where 8 is the booking ID)
    *   **Handler:** Mapped to the `cancel_booking` view.

*   **Response:**
    *   **View Logic:** The view finds the `Booking` with `pk=8`, verifies it belongs to the current user, and updates its `status` field to `'cancelled'`.
    *   **Redirect:** It redirects the user back to their profile page (`/profile/`).
    *   **Result:** The user's profile page reloads, and the booking now shows a "Cancelled" status.

---

### 10. User Logout

*   **Request:**
    *   **Action:** User clicks the "Logout" link.
    *   **Method:** `GET` (or `POST` depending on Django's configuration)
    *   **URL:** `/logout/`
    *   **Handler:** Mapped to Django's built-in `LogoutView`.

*   **Response:**
    *   **View Logic:** The `LogoutView` clears the user's session data from the server.
    *   **Redirect:** It redirects the user to the home page (`/`).
    *   **Result:** The user is logged out and sees the public home page.
