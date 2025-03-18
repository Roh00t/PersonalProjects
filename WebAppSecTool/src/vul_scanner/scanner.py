"""
scanner.py

This module defines the VulnerabilityScanner class, which coordinates various scanning techniques
to detect common web application vulnerabilities.
"""

import logging
import os
import json
from .crawler import WebCrawler
from .sql_injection_scanner import SQLInjectionScanner
from .xss_scanner import XSSScanner
from .auth_scanner import AuthScanner
from .api_security_scanner import APISecurityScanner
from .security_headers_scanner import SecurityHeadersScanner

class VulnerabilityScanner:
    """
    A comprehensive web application vulnerability scanner that integrates various scanning modules.
    """

    def __init__(self, base_url, crawl_delay=1):
        """
        Initializes the VulnerabilityScanner with the base URL and optional crawl delay.

        :param base_url: The starting URL for the scanner.
        :param crawl_delay: Delay (in seconds) between HTTP requests during crawling.
        """
        self.base_url = base_url
        self.crawl_delay = crawl_delay
        self.crawler = WebCrawler(base_url, delay=crawl_delay)
        self.scanners = {
            'sql_injection': SQLInjectionScanner(),
            'xss': XSSScanner(),
            'auth': AuthScanner(),
            'api_security': APISecurityScanner(),
            'security_headers': SecurityHeadersScanner()
        }
        self.report_path = os.path.join(os.getcwd(), "reports")
        if not os.path.exists(self.report_path):
            os.makedirs(self.report_path)
        self.logger = logging.getLogger(__name__)

    def scan(self):
        """
        Initiates the scanning process by crawling the web application and performing various vulnerability scans.
        """
        self.logger.info(f"Starting scan on: {self.base_url}")

        # Step 1: Crawl the web application to discover URLs
        discovered_urls = self.crawler.crawl()
        self.logger.info(f"Discovered {len(discovered_urls)} URLs.")

        results = []

        # Step 2: Perform vulnerability scans on each discovered URL
        for url in discovered_urls:
            self.logger.info(f"Scanning URL: {url}")
            for scan_name, scanner in self.scanners.items():
                self.logger.info(f"Running {scan_name} scan on {url}")
                result = scanner.scan(url)
                results.append(result)

        self.save_report(results)
        self.logger.info("Scanning completed.")

    def save_report(self, results):
        """
        Saves scan results to text, JSON, and HTML reports.
        """
        # Save as text
        with open(os.path.join(self.report_path, "report.txt"), "w") as txt_file:
            txt_file.write("Vulnerability Scan Report\n" + "=" * 25 + "\n")
            for result in results:
                txt_file.write(str(result) + "\n")

        # Save as JSON
        with open(os.path.join(self.report_path, "report.json"), "w") as json_file:
            json.dump(results, json_file, indent=4)

        # Save as HTML
        html_content = "<html><head><title>Scan Report</title></head><body><h1>Scan Results</h1><ul>"
        for result in results:
            html_content += f"<li>{result}</li>"
        html_content += "</ul></body></html>"

        with open(os.path.join(self.report_path, "report.html"), "w") as html_file:
            html_file.write(html_content)
        
        self.logger.info(f"Reports saved in: {self.report_path}")
