"""
crawler.py

This module defines the WebCrawler class, which is responsible for crawling web pages starting from a given URL.
It collects all reachable URLs within the same domain, which can then be analyzed for various vulnerabilities.
"""

import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import logging
import time

class WebCrawler:
    """
    A web crawler that collects all reachable URLs within the same domain starting from a given URL.
    """

    def __init__(self, base_url, delay=1):
        """
        Initializes the WebCrawler with the base URL and optional crawl delay.

        :param base_url: The starting URL for the crawler.
        :param delay: Delay (in seconds) between HTTP requests to prevent overloading the server.
        """
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.visited_urls = set()
        self.delay = delay
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        self.logger = logging.getLogger(__name__)

    def fetch_page(self, url):
        """
        Fetches the content of the given URL.

        :param url: The URL to fetch.
        :return: The content of the page, or None if the request fails.
        """
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch {url}: {e}")
            return None

    def extract_links(self, html, base_url):
        """
        Extracts and returns all unique, absolute HTTP/HTTPS links from the given HTML content.

        :param html: The HTML content of the page.
        :param base_url: The base URL to resolve relative links.
        :return: A set of absolute URLs.
        """
        soup = BeautifulSoup(html, 'html.parser')
        links = set()
        for anchor in soup.find_all('a', href=True):
            href = anchor['href']
            # Resolve relative links
            full_url = urljoin(base_url, href)
            parsed_url = urlparse(full_url)
            # Ensure the link is within the same domain and uses HTTP or HTTPS
            if parsed_url.netloc == self.base_domain and parsed_url.scheme in {'http', 'https'}:
                # Normalize the URL by removing fragments
                normalized_url = parsed_url._replace(fragment='').geturl()
                links.add(normalized_url)
        return links

    def crawl(self, url=None):
        """
        Crawls the web starting from the base URL or a specified URL, visiting each page and collecting links.

        :param url: The URL to start crawling from. If None, starts from the base URL.
        :return: A set of all visited URLs.
        """
        if url is None:
            url = self.base_url

        self.logger.info(f"Starting crawl at: {url}")
        urls_to_visit = {url}

        while urls_to_visit:
            current_url = urls_to_visit.pop()
            if current_url in self.visited_urls:
                continue

            self.logger.info(f"Visiting: {current_url}")
            self.visited_urls.add(current_url)
            html_content = self.fetch_page(current_url)

            if html_content:
                links = self.extract_links(html_content, current_url)
                urls_to_visit.update(links - self.visited_urls)

            time.sleep(self.delay)  # Respectful crawling by delaying requests

        self.logger.info(f"Crawling finished. {len(self.visited_urls)} pages visited.")
        return self.visited_urls