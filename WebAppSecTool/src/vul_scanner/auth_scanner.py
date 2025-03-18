"""
Auth Scanner
Detects weak authentication mechanisms in web applications.
"""
import requests

class AuthScanner:
    def __init__(self):
        self.name = "Authentication Scanner"

    def scan(self, url):
        print(f"Scanning {url} for weak authentication...")
        weak_creds = {"admin": "admin", "root": "toor", "user": "password"}
        for user, password in weak_creds.items():
            response = requests.post(url, data={"username": user, "password": password})
            if "Welcome" in response.text or response.status_code == 200:
                return {"url": url, "vulnerability": "Weak Credentials Found", "user": user, "password": password}
        return {"url": url, "result": "No weak authentication found"}
