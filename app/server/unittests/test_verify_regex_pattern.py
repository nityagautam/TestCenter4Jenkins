"""
    File:                   test_unit_verify_regex_pattern.py
    Author:                 @nityagautam > nityanarayan44@live.com
    Use Case:               Unit Test for verifying the regex pattern in the given string
    Date Created:           8th Sep 2021
    Last Modified:
    Modified by:

    Tests:
        - check regex pattern for simple values
        - check regex pattern for ranged values
        - check regex pattern for mixed values

    Execution:
        - python3 -m pytest -k test_unit_regex ==> Execute all the matching files
        - python3 -m pytest -m unittest        ==> Execute all the test marked unittest
	    - python3 -m pytest                    ==> Executes all available tests
"""

# Import section
import re
import pytest

# defining test data (in form of input_string, expected_string)
TEST_DATA = [
    ("(Ln:7,Col:[0-9]*,Msg:0841,Grp:[0-9])", "7, [0-9]*, 0841, [0-9]"),
    ("(Ln:1,Col:[0-9],Msg:0050,Grp:0)", "1, [0-9], 0050, 0"),
    ("(Ln:1,Col:[0-9]*,Msg:0050,Grp:5)", "1, [0-9]*, 0050, 5"),
    ("(Ln:1,Col:[0-9]*,Msg:0050,Grp:[1-5]*)", "1, [0-9]*, 0050, [1-5]*"),
    ("(Ln:[1-5],Col:[0-9]*,Msg:0050,Grp:5)", "[1-5], [0-9]*, 0050, 5"),
    ("(Ln:[1-5]*,Col:[0-9]*,Msg:0050,Grp:5)", "[1-5]*, [0-9]*, 0050, 5")
]


# Import the method to be tested
class ToTest:
    """
    This is class that's needs to be tested
    """
    def __init__(self):
        pass

    @staticmethod
    def find_txt(rgx_pattern, data, pos, is_debug=True):
        """
        Its an static member, which search for given regex pattern in a provided string
        :param rgx_pattern:
        :param data:
        :param pos:
        :param is_debug:
        :return:
        """
        _temp = re.findall(rgx_pattern, data)
        if is_debug:
            print(f"DEBUG:: Data received --> {data}, Filter reg --> {rgx_pattern}")

        try:
            return _temp[pos] if pos is not None and _temp else _temp
        except IndexError:
            raise IndexError(f"Given position={pos} does not exist")

    def get_message_pattern_from_data(self, line):
        """
        This is the caller of find_txt, which supplies regex pattern and the target string
        :param line:
        :return:
        """
        # Other working regex:  r"Ln:(.*).*,Col:(.*).*,Msg:(.*),Grp:(.*).*"
        regex_pattern = r"Ln:([0-9,\-\[\]\.\*]+),Col:([0-9,\-\[\]\.\*]+)," \
                        r"Msg:([0-9,\-\[\]\.\*]+),Grp:([0-9,\-\[\]\.\*]+)"
        return self.find_txt(regex_pattern, line, pos=0)


# Define the test with iteration over given test_data
@pytest.mark.regex
@pytest.mark.unittest
@pytest.mark.parametrize("test_string, expected", TEST_DATA)
def test_build_json_for_requirements(test_string, expected):
    """
    This is an iterative test method wrt to the TEST_DATA
    :param test_string:
    :param expected:
    :return:
    """
    line, col, msg, grp = ToTest().get_message_pattern_from_data(test_string)
    data = line + ", " + col + ", " + msg + ", " + grp
    assert data == expected, "Extracted pattern does not match"
    print(f"ASSERTION against '{test_string}', extracted: '{data}', "
          f"and expected: '{expected}' ")
