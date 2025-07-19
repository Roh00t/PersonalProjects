"""
__main__.py for the Web Vulnerability Scanner.
"""

import argparse
import logging
from .scanner import VulnerabilityScanner

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """
    Main function to parse command-line arguments and initiate the vulnerability scan.
    """
    parser = argparse.ArgumentParser(
        description='Web Vulnerability Scanner'
    )
    
    parser.add_argument(
        'url',
        type=str,
        help='Target URL to scan'
    )

    parser.add_argument(
        '--scan-type',
        type=str,
        choices=['sql', 'xss', 'auth', 'api', 'headers', 'all'],
        default='all',
        help='Type of scan to perform (default: all)'
    )

    args = parser.parse_args()

    # Initialize scanner
    scanner = VulnerabilityScanner(args.url)
    
    logger.info(f"Starting {args.scan_type.upper()} scan on {args.url}")
    
    # Run scan
    scanner.scan()

if __name__ == '__main__':
    main()