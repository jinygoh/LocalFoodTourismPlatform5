# TasteLocal Application Test Plan

This document outlines the testing strategy for the TasteLocal application, covering unit, integration, and user acceptance testing to ensure the platform is robust, reliable, and meets the project objectives.

## 1. Project Objectives

Based on the `README.md`, the primary objectives of the TasteLocal application are:
-   **For Tourists:**
    -   Discover, search, and filter local culinary offerings (dishes, shops, experiences).
    -   View listings on an interactive map.
    -   Book reservations or tours.
    -   Save favorite items to a personalized list.
    -   Read and write reviews.
    -   Manage their user profile.
-   **For Vendors:**
    -   Manage their business profile and listings.
    -   View and manage incoming bookings.

## 2. Testing Scope

The testing process will cover the following key areas of the application:
-   User authentication (registration, login, logout).
-   Core model integrity and relationships (`User`, `Shop`, `Dish`, `Experience`, `Booking`, `Review`).
-   Form validation and processing for all user inputs.
-   View logic and template rendering.
-   End-to-end user workflows for both Tourists and Vendors.
-   API endpoints (e.g., toggling favorites).
-   Performance under simulated user load.

## 3. Testing Phases

### Phase 1: Unit Testing

**Objective:** To verify that individual components (models, forms, simple functions) of the application work correctly in isolation.

**Framework:** Django's built-in `TestCase`.

**Location:** `core/tests/`

**Coverage:**
-   **Models (`test_models.py`):**
    -   Verify that model instances are created with the correct default values.
    -   Test model methods and property logic.
    -   Ensure relationships between models are correctly defined.
-   **Forms (`test_forms.py`):**
    -   Test form validation logic (e.g., required fields, data type validation).
    -   Verify that forms correctly handle valid and invalid data submissions.
    -   Check for correct widget rendering and custom styling application.

### Phase 2: Integration Testing

**Objective:** To ensure that different components of the application work together as intended.

**Framework:** Django's built-in `TestCase` and `Client`.

**Location:** `core/tests/test_views.py`

**Coverage:**
-   **Views and URL Routing:**
    -   Verify that URLs resolve to the correct views.
    -   Test that views return the expected HTTP status codes for authenticated and unauthenticated users.
    -   Ensure the correct templates are used for each view.
    -   Test view logic for both `GET` and `POST` requests, including database interactions.
    -   Verify that the context data passed to templates is accurate and complete.

### Phase 3: User Acceptance Testing (UAT)

**Objective:** To validate that the application meets the user requirements and provides a seamless user experience by testing end-to-end user flows.

**Framework:** `pytest` with `playwright`.

**Location:** `tests/e2e/`

**Coverage:**
-   **Tourist User Flow:**
    1.  User registration and login.
    2.  Searching and filtering on the Explore page.
    3.  Viewing a listing's details.
    4.  Adding/removing a listing from favorites.
    5.  Making a booking.
    6.  Submitting a review.
    7.  Editing the user profile.
-   **Vendor User Flow:**
    1.  Vendor registration and login.
    2.  Redirection to the vendor dashboard.
    3.  Updating the business profile.
    4.  Creating and managing dish and experience listings.
    5.  Viewing incoming bookings.

### Phase 4: Performance Testing

**Objective:** To assess the application's responsiveness, stability, and scalability under load.

**Tools:** `django-debug-toolbar` and `locust`.

**Methodology:**
-   **Code Profiling:** Use `django-debug-toolbar` to analyze database query performance and identify bottlenecks in key views (e.g., Explore page with complex filtering).
-   **Load Testing:** Use `locust` to simulate a realistic number of concurrent users browsing the site, searching for listings, and making bookings.
-   **Metrics:**
    -   Page load times.
    -   Database query count and execution time.
    -   Server response time under load.
    -   Error rate during load tests.

## 4. Documentation and Reporting

-   **Test Results (`docs/TEST_RESULTS.md`):** A summary of the execution results from all testing phases, including a compliance table mapping results to project objectives.
-   **Issue Log (`docs/ISSUE_LOG.md`):** A detailed log of all identified defects, including their severity, impact, and the plan for corrective action.
-   **Performance Analysis (`docs/PERFORMANCE_ANALYSIS.md`):** A report on performance test findings, including identified bottlenecks and optimization recommendations.
-   **Recommendations (`docs/RECOMMENDATIONS.md`):** A final document summarizing key findings and providing recommendations for future enhancements.
