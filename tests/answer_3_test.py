import unittest
from answer_3 import (
    _validate_board_size,
    _calculate_paths_to_position,
    _calculate_combinations_without_looping,
    analyze_board_game
)
from constants.errors import ERROR_BOARD_SIZE_LESS_THAN_THREE


class TestValidateBoardSize(unittest.TestCase):
    """Test cases for _validate_board_size function."""

    def test_valid_size(self):
        """Tests that valid sizes do not raise an exception."""
        _validate_board_size(3)
        _validate_board_size(13)

    def test_invalid_size(self):
        """Tests that a size less than 3 raises ValueError."""
        with self.assertRaises(ValueError) as context:
            _validate_board_size(2)
        self.assertEqual(str(context.exception), ERROR_BOARD_SIZE_LESS_THAN_THREE)

class TestCalculatePathsToPosition(unittest.TestCase):
    """Test cases for _calculate_paths_to_position function."""

    def test_base_case(self):
        """Tests the base case: position 1 in 0 turns returns 1."""
        self.assertEqual(_calculate_paths_to_position(1, 0), 1)

    def test_invalid_position(self):
        """Tests that position less than 1 returns 0."""
        self.assertEqual(_calculate_paths_to_position(0, 1), 0)
        self.assertEqual(_calculate_paths_to_position(-5, 3), 0)

    def test_zero_turn_position_greater_than_one(self):
        """Tests that turn 0 with position greater than 1 returns 0."""
        self.assertEqual(_calculate_paths_to_position(2, 0), 0)
        self.assertEqual(_calculate_paths_to_position(5, 0), 0)

    def test_negative_turn(self):
        """Tests that negative turn returns 0."""
        self.assertEqual(_calculate_paths_to_position(0, -1), 0)
        self.assertEqual(_calculate_paths_to_position(3, -2), 0)

    def test_simple_path_one_turn(self):
        """Tests paths in 1 turn."""
        self.assertEqual(_calculate_paths_to_position(2, 1), 1)  # jump 1 (1->2)
        self.assertEqual(_calculate_paths_to_position(3, 1), 1)  # jump 2 (1->3)
        self.assertEqual(_calculate_paths_to_position(4, 1), 1)  # jump 3 (1->4)
        self.assertEqual(_calculate_paths_to_position(5, 1), 0)  # impossible

    def test_path_two_turns(self):
        """Tests paths in 2 turns."""
        self.assertEqual(_calculate_paths_to_position(3, 2), 1)  # 1+1 (1->2->3)
        self.assertEqual(_calculate_paths_to_position(4, 2), 2)  # 1+2, 2+1
        self.assertEqual(_calculate_paths_to_position(5, 2), 3)  # 1+3, 2+2, 3+1
        self.assertEqual(_calculate_paths_to_position(6, 2), 2)  # 2+3, 3+2
        self.assertEqual(_calculate_paths_to_position(7, 2), 1)  # 3+3

    def test_path_three_turns(self):
        """Tests paths in 3 turns."""
        self.assertEqual(_calculate_paths_to_position(4, 3), 1)  # 1+1+1 (1->2->3->4)
        self.assertEqual(_calculate_paths_to_position(5, 3), 3)  # 1+1+2, 1+2+1, 2+1+1
        self.assertEqual(_calculate_paths_to_position(7, 3), 7)  # various combinations


class TestCalculateCombinationsWithoutLooping(unittest.TestCase):
    """Test cases for _calculate_combinations_without_looping function."""

    def test_three_positions(self):
        """Tests board with 3 positions"""
        self.assertEqual(_calculate_combinations_without_looping(3), 2)  # 1+1, 2

    def test_four_positions(self):
        """Tests board with 4 positions"""
        self.assertEqual(_calculate_combinations_without_looping(4), 4)  # 1+1+1, 1+2, 2+1, 3

    def test_five_positions(self):
        """Tests board with 5 positions"""
        self.assertEqual(_calculate_combinations_without_looping(5), 7)

    def test_six_positions(self):
        """Tests board with 6 positions"""
        self.assertEqual(_calculate_combinations_without_looping(6), 13)

    def test_seven_positions(self):
        """Tests board with 7 positions"""
        self.assertEqual(_calculate_combinations_without_looping(7), 24)

    def test_eight_positions(self):
        """Tests board with 8 positions"""
        self.assertEqual(_calculate_combinations_without_looping(8), 44)

    def test_nine_positions(self):
        """Tests board with 9 positions"""
        self.assertEqual(_calculate_combinations_without_looping(9), 81)


class TestBoardGame(unittest.TestCase):
    """Test cases for analyze_board_game function."""

    def test_minimum_size(self):
        """Tests board with minimum size (3 positions, positions 1, 2, 3)."""
        result = analyze_board_game(3)
        self.assertEqual(result.min_turns, 1)
        self.assertAlmostEqual(result.optimal_probability, 1/3)
        self.assertEqual(result.combinations_without_looping, 2)

    def test_seven_positions(self):
        """For 7 positions (positions 1-7). Optimal: 2 turns.
        Combinations: 24"""
        result = analyze_board_game(7)
        self.assertEqual(result.min_turns, 2)
        self.assertAlmostEqual(result.optimal_probability, 1/9)
        self.assertEqual(result.combinations_without_looping, 24)

    def test_eight_positions(self):
        """For 8 positions (positions 1-8). Optimal: 3 turns.
        Combinations: 44"""
        result = analyze_board_game(8)
        self.assertEqual(result.min_turns, 3)
        self.assertAlmostEqual(result.optimal_probability, 6/27)
        self.assertEqual(result.combinations_without_looping, 44)

    def test_error_invalid_input(self):
        """Tests that invalid input raises ValueError."""
        with self.assertRaises(ValueError) as context:
            analyze_board_game(2)
        self.assertEqual(str(context.exception), ERROR_BOARD_SIZE_LESS_THAN_THREE)

    def test_error_zero_input(self):
        """Tests that input 0 raises ValueError."""
        with self.assertRaises(ValueError) as context:
            analyze_board_game(0)
        self.assertEqual(str(context.exception), ERROR_BOARD_SIZE_LESS_THAN_THREE)

    def test_error_negative_input(self):
        """Tests that negative input raises ValueError."""
        with self.assertRaises(ValueError) as context:
            analyze_board_game(-5)
        self.assertEqual(str(context.exception), ERROR_BOARD_SIZE_LESS_THAN_THREE)