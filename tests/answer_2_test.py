import unittest
from answer_2 import _validate_position, get_sequence_value
from constants.errors import ERROR_POSITION_LESS_THAN_ONE


class TestValidatePosition(unittest.TestCase):
    """Test cases for _validate_position function."""

    def test_valid_positions(self):
        """Tests some valid positive positions."""
        _validate_position(1)
        _validate_position(10)

    def test_position_zero(self):
        """Tests that position 0 raises ValueError with correct message."""
        with self.assertRaises(ValueError) as context:
            _validate_position(0)
        self.assertEqual(str(context.exception), ERROR_POSITION_LESS_THAN_ONE)

    def test_negative_position(self):
        """Tests that a negative position raises ValueError."""
        with self.assertRaises(ValueError) as context:
            _validate_position(-1)
        self.assertEqual(str(context.exception), ERROR_POSITION_LESS_THAN_ONE)


class TestNumericSequence(unittest.TestCase):
    """Test cases for get_sequence_value function."""

    def test_valid_positions(self):
        """Tests several valid positions in the sequence."""
        self.assertEqual(get_sequence_value(1), 11)
        self.assertEqual(get_sequence_value(2), 18)
        self.assertEqual(get_sequence_value(200), 1404)
        self.assertEqual(get_sequence_value(254), 1782)
        self.assertEqual(get_sequence_value(3542158), 24795110)

    def test_invalid_position(self):
        """Ensures that the correct exception and external message are raised."""
        with self.assertRaises(ValueError) as context:
            get_sequence_value(0)
        self.assertEqual(str(context.exception), ERROR_POSITION_LESS_THAN_ONE)