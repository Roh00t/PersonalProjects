import unittest
from unittest.mock import patch, Mock
from src.vul_scanner.scanner import scan_for_vulnerabilities  # Replace with your actual import

class TestScanner(unittest.TestCase):

    @patch('src.vul_scanner.scanner.requests.get')
    def test_scan_for_vulnerabilities(self, mock_get):
        # Simulate a successful HTTP response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = '<html><body><input name="username"><input name="password"></body></html>'
        mock_get.return_value = mock_response

        # Call the function you're testing
        result = scan_for_vulnerabilities('http://localhost:3000')

        # Assertions to verify the behavior
        self.assertIn('Potential sensitive information exposure', result)
        self.assertEqual(len(result), 1)

if __name__ == '__main__':
    unittest.main()