"""
utils.py

This module provides utility functions to support the vulnerability scanner's operations.
"""

import re
import logging
from urllib.parse import urlparse, parse_qs

def is_valid_url(url):
    """
    Validates if the provided string is a well-formed URL.

    :param url: The URL string to validate.
    :return: True if the URL is valid, False otherwise.
    """
    regex = re.compile(
        r'^(?:http|https)://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def extract_url_parameters(url):
    """
    Extracts query parameters from a URL.

    :param url: The URL string to extract parameters from.
    :return: A dictionary of query parameters and their values.
    """
    parsed_url = urlparse(url)
    return parse_qs(parsed_url.query)

def configure_logging(log_level=logging.INFO, log_file=None):
    """
    Configures logging for the application.

    :param log_level: The logging level (e.g., logging.INFO, logging.DEBUG).
    :param log_file: Optional file path to log to a file. If None, logs to console.
    """
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    if log_file:
        logging.basicConfig(level=log_level, format=log_format, filename=log_file)
    else:
        logging.basicConfig(level=log_level, format=log_format)

def sanitize_input(user_input):
    """
    Sanitizes user input to prevent injection attacks.

    :param user_input: The input string to sanitize.
    :return: A sanitized version of the input string.
    """
    return re.sub(r'[^\w\s-]', '', user_input)

def is_ip_address(address):
    """
    Checks if the provided string is a valid IP address.

    :param address: The string to check.
    :return: True if the string is a valid IP address, False otherwise.
    """
    try:
        socket.inet_aton(address)
        return True
    except socket.error:
        return False