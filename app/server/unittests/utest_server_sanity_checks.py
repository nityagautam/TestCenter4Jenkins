"""
  @author Ashutosh Mishra (@github: nityagautam)

  Software Engineer & Explorer
  nityanarayan44@gmail.com

  Created on 14 February, 2023 @ 10:25 AM.
  Copyright © 2018. Victor. All rights reserved.
"""


# Import Section
# ==========================
import os
import unittest


class TestSanity(unittest.TestCase):
    def test_dir_check(self):
        assert True is not False, "True is False"

    def test_sanity_check(self):
        assert 1 < 2, "1 is greater than 2"

    @staticmethod
    def print_notice(self):
        print("""
                ======================= IMPORTANT =========================
                To Run the ReportServer unit test cases it is required to:
                1) Flask Server is running (Now Optional);
                2) Required Dirs exist;
                3) Required Python3 modules are installed;
                4) Python 3 is in the path.""")
        print("====================== STARTING =======================\n")

    def get_testsuite(self):
        suite = unittest.TestSuite()
        suite.addTest(TestSanity('test_sanity_check'))
        suite.addTest(TestSanity('test_dir_check'))
        # Let's say If I add more test methods, then I will add more of the above lines
        return self.suite


if __name__ == '__main__':
    # Test Suite Execution
    runner = unittest.TextTestRunner()
    runner.run(TestSanity().get_testsuite())
