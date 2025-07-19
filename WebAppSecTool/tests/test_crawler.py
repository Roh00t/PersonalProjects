import unittest
from unittest.mock import patch, Mock
from src.vul_scanner.crawler import crawl_function  # Replace with your actual import

class TestCrawler(unittest.TestCase):

    @patch('src.vul_scanner.crawler.requests.get')
    def test_crawl_function(self, mock_get):
        # Simulate a successful HTTP response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '<html><body><a href="http://localhost:3000/page1">Page 1</a></body></html>'
        mock_get.return_value = mock_response

        # Call the function you're testing
        result = crawl_function('http://localhost:3000')

        # Assertions to verify the behavior
        self.assertIn('http://localhost:3000/page1', result)
        self.assertEqual(len(result), 1)

if __name__ == '__main__':
    unittest.main()