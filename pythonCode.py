from locust import HttpUser, task, between
from bs4 import BeautifulSoup


class SecureServerUser(HttpUser):
    wait_time = between(1, 3)  # Wait between 1 and 3 seconds between tasks

    def on_start(self):
        """Runs at the start of each simulated user session."""
        self.login()

    def bypass_captcha(self, captcha_image):
        """Bypass CAPTCHA by decoding or using a mock solver."""
        # Mock CAPTCHA solver: In a real scenario, implement logic to solve the CAPTCHA.
        # For now, returning a fixed string assuming CAPTCHA is static for tests.
        return "mock_captcha_solution"

    def login(self):
        """Perform login by handling the CSRF token."""
        # Step 1: Get the login page to retrieve the CSRF token
        response = self.client.get("/login")
        print(f"GET login: {response.status_code}")

        if response.status_code == 200:
            # Parse the CSRF token and CAPTCHA using BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")
            csrf_token = soup.find("input", attrs={"name": "csrf_token"})
            captcha_image = soup.find("img", attrs={"id": "captcha_image"})

            if csrf_token and captcha_image:
                csrf_token_value = csrf_token["value"]

                # Simulate CAPTCHA solving
                captcha_solution = self.bypass_captcha(captcha_image)

                # Step 2: Send a POST request to log in
                login_data = {
                    "username": "admin",
                    "password": "123456",
                    "csrf_token": csrf_token_value,
                    "captcha": captcha_solution
                }

                login_response = self.client.post("/login", data=login_data)
                print(f"POST /login: {login_response.status_code}")
            else:
                print("CSRF token or CAPTCHA not found on the login page.")
        else:
            print("Failed to fetch the login page.")

    @task(1)
    def view_home_page(self):
        """Simulate viewing the home page."""
        response = self.client.get("/home")
        print(f"GET /home: {response.status_code}")

    @task(2)
    def view_login_audit_report(self):
        """Simulate navigating to and viewing the 'Login Audit Report' submodule."""
        # Simulate navigation to the 'Login Audit Report' submodule
        report_page_response = self.client.get("/report/system/getUserLogin")
        print(f"GET /report/system/getUserLogin: {report_page_response.status_code}")

