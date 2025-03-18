"""
API Security Scanner
Scans for misconfigured API endpoints and security risks.
"""
import requests

class APISecurityScanner:
    def __init__(self):
        self.name = "API Security Scanner"

    def scan(self, url):
        print(f"Scanning {url} for API security issues...")
        headers = {"Authorization": "Bearer test_token"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200 and "sensitive_data" in response.text:
            return {"url": url, "vulnerability": "Exposed Sensitive API Data"}
        return {"url": url, "result": "No API security issues found"}
