"""
XSS Scanner
Detects potential Cross-Site Scripting (XSS) vulnerabilities in web applications.
"""
import requests
import re

class XSSScanner:
    def __init__(self):
        self.name = "Cross-Site Scripting (XSS) Scanner"

    def scan(self, url):
        print(f"Scanning {url} for XSS vulnerabilities...")
        payloads = ["<script>alert('XSS')</script>", "<img src=x onerror=alert('XSS')>"]
        for payload in payloads:
            response = requests.get(url, params={"input": payload})
            if payload in response.text:
                return {"url": url, "vulnerability": "XSS Found", "payload": payload}
        return {"url": url, "result": "No vulnerabilities found"}