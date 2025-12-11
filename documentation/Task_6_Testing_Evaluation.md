# Task 6: Testing and Evaluation

## 1. Test Plan & Results

| Test Case ID | Description | Type | Expected Result | Actual Result | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-001** | User Registration | Functional | User account created in DB. | User created successfully. | **PASS** |
| **TC-002** | Vendor Profile Creation | Functional | Vendor linked to User. | Vendor profile linked. | **PASS** |
| **TC-003** | Home Page Load | UI/UX | Page loads with Hero section. | Page loads (HTTP 200). | **PASS** |
| **TC-004** | Login Page Load | UI/UX | Login form displayed. | Form displayed (HTTP 200). | **PASS** |
| **TC-005** | Database Integrity | Integration | Foreign keys maintained. | Integrity maintained. | **PASS** |

## 2. Performance Testing
*   **Load Time:** The application loads in under 200ms on local environment.
*   **Optimization:** Static assets (CSS) are lightweight. Images are currently placeholders (external URLs) to save bandwidth.

## 3. Recommendations for Future
1.  **AJAX Search:** Implement real-time search without page reloads.
2.  **Map Integration:** Add Google Maps or Leaflet for visual location of vendors.
3.  **Payment Gateway:** Integrate Stripe/PayPal for real bookings.
