"""
__init__.py for vul_scanner package.
"""

import logging
from flask import Flask

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Initializing the vul_scanner package.")

# Initialize Flask application
app = Flask(__name__)

@app.route('/')
def home():
    return "Web Vulnerability Scanner is running!"

# Import scanner modules (ensure they exist)
from .scanner import VulnerabilityScanner
from .crawler import WebCrawler
from .sql_injection_scanner import SQLInjectionScanner
from .xss_scanner import XSSScanner
from .auth_scanner import AuthScanner
from .api_security_scanner import APISecurityScanner
from .security_headers_scanner import SecurityHeadersScanner
from .reporter import Reporter
from .utils import *

__all__ = ['app', 'VulnerabilityScanner', 'WebCrawler', 'SQLInjectionScanner', 'XSSScanner', 'AuthScanner', 'APISecurityScanner', 'SecurityHeadersScanner', 'Reporter']