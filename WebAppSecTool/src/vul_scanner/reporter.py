"""
reporter.py

This module defines the Reporter class, responsible for aggregating vulnerability scan results
and generating reports in various formats.
"""

import json
import logging
from datetime import datetime

class Reporter:
    """
    Aggregates vulnerability scan results and generates reports in various formats.
    """

    def __init__(self):
        """
        Initializes the Reporter with an empty list to store findings.
        """
        self.findings = []
        self.logger = logging.getLogger(__name__)

    def add_finding(self, url, vulnerability_type, description, severity):
        """
        Adds a new finding to the report.

        :param url: The URL where the vulnerability was found.
        :param vulnerability_type: The type of vulnerability (e.g., 'SQL Injection', 'XSS').
        :param description: A detailed description of the vulnerability.
        :param severity: The severity level of the vulnerability (e.g., 'Low', 'Medium', 'High').
        """
        finding = {
            'url': url,
            'vulnerability_type': vulnerability_type,
            'description': description,
            'severity': severity,
            'timestamp': datetime.utcnow().isoformat()
        }
        self.findings.append(finding)
        self.logger.info(f"Added finding: {finding}")

    def generate_text_report(self):
        """
        Generates a plain text report of the findings.

        :return: A string containing the plain text report.
        """
        report_lines = ["Vulnerability Scan Report", "=" * 25, ""]
        for finding in self.findings:
            report_lines.append(f"URL: {finding['url']}")
            report_lines.append(f"Vulnerability: {finding['vulnerability_type']}")
            report_lines.append(f"Description: {finding['description']}")
            report_lines.append(f"Severity: {finding['severity']}")
            report_lines.append(f"Timestamp: {finding['timestamp']}")
            report_lines.append("-" * 40)
        return "\n".join(report_lines)

    def generate_json_report(self):
        """
        Generates a JSON report of the findings.

        :return: A JSON-formatted string containing the report.
        """
        return json.dumps(self.findings, indent=4)

    def generate_html_report(self):
        """
        Generates an HTML report of the findings.

        :return: A string containing the HTML report.
        """
        html = ["<html><head><title>Vulnerability Scan Report</title></head><body>"]
        html.append("<h1>Vulnerability Scan Report</h1>")
        html.append("<table border='1'><tr><th>URL</th><th>Vulnerability</th><th>Description</th><th>Severity</th><th>Timestamp</th></tr>")
        for finding in self.findings:
            html.append("<tr>")
            html.append(f"<td>{finding['url']}</td>")
            html.append(f"<td>{finding['vulnerability_type']}</td>")
            html.append(f"<td>{finding['description']}</td>")
            html.append(f"<td>{finding['severity']}</td>")
            html.append(f"<td>{finding['timestamp']}</td>")
            html.append("</tr>")
        html.append("</table></body></html>")
        return "\n".join(html)

    def save_report(self, filename, format='text'):
        """
        Saves the report to a file in the specified format.

        :param filename: The name of the file to save the report to.
        :param format: The format of the report ('text', 'json', 'html').
        """
        if format == 'text':
            report_content = self.generate_text_report()
        elif format == 'json':
            report_content = self.generate_json_report()
        elif format == 'html':
            report_content = self.generate_html_report()
        else:
            self.logger.error(f"Unsupported report format: {format}")
            raise ValueError(f"Unsupported report format: {format}")

        with open(filename, 'w') as report_file:
            report_file.write(report_content)
        self.logger.info(f"Report saved to {filename} in {format} format.")