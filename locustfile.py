from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        # First, we need to get the CSRF token. Django sets this in a cookie.
        self.client.get("/login/")
        csrftoken = self.client.cookies['csrftoken']

        # Now we can log in with the CSRF token.
        self.client.post("/login/", {
            "username": "tourist_john",
            "password": "TestPass123!",
            "csrfmiddlewaretoken": csrftoken
        }, headers={"X-CSRFToken": csrftoken, "Referer": self.client.base_url + "/login/"})

    @task
    def home_page(self):
        self.client.get("/")

    @task(3)
    def explore_page(self):
        self.client.get("/explore/")

    @task(2)
    def profile_page(self):
        self.client.get("/profile/")
