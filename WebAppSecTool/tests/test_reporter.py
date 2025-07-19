import unittest
import HtmlTestRunner
# html-testRunner is a test runner that saves the test results in HTML format.


class MyTestCase(unittest.TestCase):
    def test_case_1(self):
        self.assertEqual(2, 2, "Test Passed")

    def test_case_2(self):
        self.assertEqual(2, 3, "Test Failed")  # This test will fail

    def test_case_3(self):
        self.assertEqual(2, 5, "Test Failed")  # This test will fail

    def test_case_4(self):
        self.assertEqual(2, 1, "Test Failed")  # This test will fail

    def test_case_5(self):
        pass  # This test will be marked as 'passed'

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='test_reports'))
