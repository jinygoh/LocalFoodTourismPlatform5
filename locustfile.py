from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.client.post("/login/", {
            "username": "tourist_john",
            "password": "TestPass123!"
        })

    @task
    def home_page(self):
        self.client.get("/")

    @task(3)
    def explore_page(self):
        self.client.get("/explore/")

    @task(2)
    def profile_page(self):
        self.client.get("/profile/")
