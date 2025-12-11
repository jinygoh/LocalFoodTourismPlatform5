# TasteLocal Application Performance Analysis

This document outlines the performance testing and analysis conducted on the TasteLocal application.

## 1. Performance Testing Tools

The following tools were used for performance testing:

-   **Django Debug Toolbar:** For in-browser profiling of database queries, template rendering times, and other request-related details.
-   **Locust:** For load testing the application with simulated concurrent users.

## 2. Setup and Configuration

### Django Debug Toolbar

The Django Debug Toolbar was installed and configured for the project. This involved:
1.  Installing the `django-debug-toolbar` package.
2.  Adding `'debug_toolbar'` to the `INSTALLED_APPS` in `settings.py`.
3.  Adding the `DebugToolbarMiddleware` to the `MIDDLEWARE` in `settings.py`.
4.  Configuring the `INTERNAL_IPS` to allow the toolbar to be displayed in development.
5.  Adding the toolbar's URL patterns to the project's `urls.py`.

### Locust

Locust was installed, and a `locustfile.py` was created to define the user behavior for the load tests. The test simulates users logging in and then browsing the home, explore, and profile pages.

## 3. How to Run Performance Tests

### Django Debug Toolbar

1.  Ensure `DEBUG` is set to `True` in `settings.py`.
2.  Run the Django development server: `python manage.py runserver`
3.  Access any page in the application. The Debug Toolbar will be visible on the right side of the screen, providing detailed performance information for each request.

### Locust

1.  **Start the Target Server:** Ensure the Django development server is running.
    ```bash
    python manage.py runserver
    ```
    This server will be the target of our load test.

2.  **Start Locust:** In a *separate* terminal, start the Locust service.
    ```bash
    locust
    ```

3.  **Open the Locust Web Interface:** Open your web browser and navigate to the Locust dashboard, which runs on its own server.
    `http://localhost:8089`

4.  **Configure and Start the Load Test:** You will see a "Start new load test" screen. Here’s what to enter for a baseline test:

    *   **Number of users (peak concurrency):** This is the maximum number of users you want to simulate. A good starting point is **`100`**.
    *   **Ramp up (users started/second):** This determines how quickly your users are created. To avoid overwhelming the server instantly, start with a gradual rate, such as **`10`**. This means Locust will add 10 new users every second until it reaches the 100-user peak.
    *   **Host:** This is the most important field. You must provide the full URL of the application you are testing. For a local development server, this will be **`http://127.0.0.1:8000`**.

    Leave the "Run time" field blank for a basic test that you stop manually.

    Once configured, click the **"Start swarming"** button. Locust will begin simulating users, and you will see real-time statistics on the next page.

## 4. Performance Analysis and Findings

Due to limitations in the current environment, I was not able to run the Locust load tests and generate a performance report. However, the setup is in place for future performance testing.

The Django Debug Toolbar is a valuable tool for identifying performance bottlenecks during development. By inspecting the query counts and execution times for each request, developers can identify and optimize slow queries and inefficient code paths.

## 5. Recommendations

-   **Regular Performance Testing:** It is recommended to run the Locust load tests regularly to identify performance regressions as the application evolves.
-   **Database Query Optimization:** Use the Django Debug Toolbar to identify and optimize slow database queries. This may involve adding database indexes, using `select_related` and `prefetch_related` to reduce the number of queries, and caching frequently accessed data.
-   **Frontend Performance:** Analyze the frontend performance of the application using browser developer tools. This includes optimizing image sizes, minifying CSS and JavaScript, and leveraging browser caching.
