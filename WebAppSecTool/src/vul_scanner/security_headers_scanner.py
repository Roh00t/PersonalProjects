"""
Security Headers Scanner
Checks if the web application has proper security headers.
"""
import requests

class SecurityHeadersScanner:
    def __init__(self):
        self.name = "Security Headers Scanner"

    def scan(self, url):
        print(f"Checking security headers for {url}...")
        response = requests.get(url)
        missing_headers = []
        required_headers = ["Content-Security-Policy", "X-Frame-Options", "Strict-Transport-Security"]
        for header in required_headers:
            if header not in response.headers:
                missing_headers.append(header)
        if missing_headers:
            return {"url": url, "vulnerability": "Missing Security Headers", "headers": missing_headers}
        return {"url": url, "result": "All security headers present"}
