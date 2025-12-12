"""
This file is a Locust test script (a "locustfile") used for performance testing
the TasteLocal web application.

Locust is an open-source load testing tool that allows you to define user behavior
with Python code and swarm your system with millions of simultaneous users.

This script defines a `WebsiteUser` that simulates a logged-in tourist browsing
key pages of the site.

To run this test, you would use the `locust` command from your terminal:
`locust -f locustfile.py --host=http://127.0.0.1:8000`
"""
from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    """
    A class representing a single user (a "locust") that will be spawned.
    It inherits from HttpUser, which gives it a `client` attribute to make HTTP requests.
    """
    # `wait_time` defines a random wait time between 1 and 5 seconds for each user
    # between the execution of tasks. This simulates real user behavior.
    wait_time = between(1, 5)

    def on_start(self):
        """
        This method is called once for each simulated user when they start.
        It's used here to handle the login process, as we want to simulate the
        behavior of a logged-in user.
        """
        # --- Django CSRF Handling ---
        # Django's login form is protected by a CSRF (Cross-Site Request Forgery) token.
        # To successfully log in, we must first fetch the login page to get the
        # `csrftoken` cookie, and then include that token in our POST request.

        # 1. Make a GET request to the login page to get the CSRF cookie.
        self.client.get("/login/")

        # 2. Extract the CSRF token from the session cookies.
        csrftoken = self.client.cookies.get('csrftoken')

        # 3. Make a POST request to the login URL with the user's credentials
        #    and the necessary CSRF headers. The user 'tourist_john' is created
        #    by the `populate_test_data.py` script.
        self.client.post("/login/", {
            "username": "tourist_john",
            "password": "TestPass123!",
            "csrfmiddlewaretoken": csrftoken
        }, headers={
            "X-CSRFToken": csrftoken,
            "Referer": self.client.base_url + "/login/"
        })

    @task
    def home_page(self):
        """
        Defines a user task to visit the home page. The `@task` decorator
        marks this method as a task that Locust will pick and execute.
        By default, it has a weight of 1.
        """
        self.client.get("/")

    @task(3)
    def explore_page(self):
        """
        Defines a task to visit the explore page. The number in the decorator `(3)`
        is the task's weight. This means that a user is 3 times more likely
        to execute this task than the `home_page` task.
        """
        self.client.get("/explore/")

    @task(2)
    def profile_page(self):
        """
        Defines a task to visit the profile page with a weight of 2.
        """
        self.client.get("/profile/")
