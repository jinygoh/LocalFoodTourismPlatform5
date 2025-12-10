# How to Run the TasteLocal Test Suite

This document provides step-by-step instructions for running the automated tests for the TasteLocal application from your terminal.

## 1. Prerequisites

Before you begin, ensure you have completed the full project setup as described in the main `README.md` file. This includes:
-   Cloning the repository.
-   Creating and activating a Python virtual environment.
-   Installing all dependencies from `requirements.txt`.
-   Setting up the MySQL database and configuring your `.env` file.

## 2. Setting Up the Testing Environment

The testing environment has a few specific dependencies, including system packages for `mysqlclient` and the Playwright browser automation tool.

### Step 2.1: Install System Dependencies for MySQL

If you have not already done so during the initial setup, you must install the MySQL client development headers.

```bash
# On Debian/Ubuntu
sudo apt-get update
sudo apt-get install -y default-libmysqlclient-dev build-essential mysql-server
```

### Step 2.2: Install and Configure Playwright

The end-to-end tests use Playwright. You need to install its system dependencies and browser binaries.

```bash
# Install the pytest plugin
pip install pytest-playwright

# Install the necessary system dependencies
sudo python -m playwright install-deps

# Install the browser binaries (Chromium, Firefox, WebKit)
playwright install
```

### Step 2.3: Start the MySQL Service

The tests require an active connection to a MySQL database. Ensure the service is running.

```bash
# Start the MySQL service
sudo service mysql start
```

### Step 2.4: Create the Database

The application needs a database named `tastelocal` to exist. The test runner will create a separate, temporary database for its own use during execution.

```bash
# Create the main database if it doesn't exist
sudo mysql -u root -e "CREATE DATABASE IF NOT EXISTS tastelocal;"
```

## 3. Running the Tests

The project contains two main test suites: one for the Django backend (unit and integration tests) and one for the frontend (end-to-end tests).

### Step 3.1: Running Backend Tests (Unit & Integration)

These tests check the application's core logic, models, forms, and views without needing a running web server.

```bash
# Run the core application's test suite
python manage.py test core
```

**Expected Output (Success):**
You should see output indicating that the test database is being created, followed by a series of dots (`.......`) representing each successful test. The final output should look like this:

```
.......
----------------------------------------------------------------------
Ran 7 tests in X.XXXs

OK
Destroying test database for alias 'default'...
```

### Step 3.2: Running Frontend Tests (End-to-End)

These tests simulate real user interactions in a browser and require a running instance of the Django development server.

**First, start the development server in the background:**

```bash
python manage.py runserver > server.log 2>&1 &
```

**Then, run the E2E test suite:**

```bash
DJANGO_ALLOW_ASYNC_UNSAFE=true pytest -v tests/e2e/
```

**Expected Output (Current State - Failing):**
As noted in the `TEST_RESULTS.md`, the E2E test environment is currently unstable. **You should expect to see several tests failing with `TimeoutError` messages.** This is a known issue. A successful run in the future would look like this:

```
============================= test session starts ==============================
...
tests/e2e/test_cancel_booking.py::test_cancel_booking[chromium] PASSED   [ 11%]
tests/e2e/test_homepage.py::test_homepage_elements_are_visible[chromium] PASSED [ 22%]
...
========================= 9 passed in XXX.XXs ==========================
```

## 4. Cleaning Up

After running the E2E tests, you can stop the background development server.

```bash
# Find and kill the server process running on port 8000
kill $(lsof -t -i :8000) 2>/dev/null || true
```
