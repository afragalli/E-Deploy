import unittest
from answer_1 import check_b_a_pattern


class TestCheckPattern(unittest.TestCase):
    """Test cases for check_b_a_pattern function."""

    def test_positive_cases(self):
        """Tests strings that perfectly meet the criteria."""
        self.assertTrue(check_b_a_pattern("BALA"))
        self.assertTrue(check_b_a_pattern("BOLA"))
        self.assertTrue(check_b_a_pattern("BA"))

    def test_negative_cases(self):
        """Tests strings that fail in one or both criteria."""
        self.assertFalse(check_b_a_pattern("ALBA"))
        self.assertFalse(check_b_a_pattern("BOLO"))
        self.assertFalse(check_b_a_pattern("ABACAXI"))

    def test_case_sensitivity(self):
        """Tests if the function is case-sensitive."""
        self.assertFalse(check_b_a_pattern("bala"))
        self.assertFalse(check_b_a_pattern("Bala"))
        self.assertFalse(check_b_a_pattern("balA"))

    def test_empty_or_short_string(self):
        """Tests behavior with empty or single-character strings."""
        self.assertFalse(check_b_a_pattern(""))
        self.assertFalse(check_b_a_pattern("B"))
        self.assertFalse(check_b_a_pattern("A"))