from dataclasses import dataclass
from constants.errors import ERROR_BOARD_SIZE_LESS_THAN_THREE

@dataclass(frozen=True)
class GameStatistics:
    """Stores the board analysis results.

    Attributes:
        min_turns: Minimum number of turns required to reach the last position
            using only jumps of 1, 2, or 3 positions.
        optimal_probability: Probability of reaching the last position in the
            minimum number of turns, assuming each jump (1, 2, or 3) has equal
            probability (1/3). Calculated as optimal_paths / (3^min_turns).
        combinations_without_looping: Total number of valid jump sequences
            (combinations) that reach the last position without looping,
            regardless of the number of turns taken.
    """
    min_turns: int
    optimal_probability: float
    combinations_without_looping: int


def _validate_board_size(num_positions: int) -> None:
    """
    Validates if the board size is valid.

    Args:
        num_positions (int): Total number of positions on the board.

    Raises:
        ValueError: If num_positions is less than 3.
    """
    if num_positions < 3:
        raise ValueError(ERROR_BOARD_SIZE_LESS_THAN_THREE)


def _calculate_paths_to_position(position: int, turn: int) -> int:
    """
    Calculates the number of paths to reach a position in exactly N turns.

    Recursive function that counts all jump sequences
    (1, 2 or 3 positions) that allow reaching position 'position' exactly after
    'turn' moves, starting from position 1.

    Args:
        position (int): Destination position (1-indexed). Must be positive.
        turn (int): Exact number of turns to reach the position. Must be non-negative.

    Returns:
        int: Number of valid paths to reach 'position' in exactly 'turn' turns.
             Returns 0 if it's not possible to reach the position with the specified number of turns.
    """
    if position == 1 and turn == 0:
        return 1
    if position < 1 or turn <= 0:
        return 0

    total = 0
    for jump in (1, 2, 3):
        total += _calculate_paths_to_position(position - jump, turn - 1)
    return total


def _calculate_combinations_without_looping(num_positions: int) -> int:
    """
    Calculates the total combinations without looping to reach the last position.

    Uses optimized dynamic programming (tribonacci) to count all jump sequences
    (1, 2 or 3 positions) that allow reaching the last position (num_positions)
    in any number of turns, without looping.

    Args:
        num_positions (int): Total number of positions on the board.

    Returns:
        int: Total number of combinations without looping to reach the last position.
    """
    if num_positions in [1, 2]:
        return 1
    if num_positions == 3:
        return 2

    a, b, c = 1, 1, 2

    for _ in range(4, num_positions + 1):
        next_val = a + b + c
        a, b, c = b, c, next_val

    return c

def analyze_board_game(num_positions: int) -> GameStatistics:
    """
    Analyzes the statistics of an unidirectional board game.

    Args:
        num_positions (int): Total number of positions on the board.

    Returns:
        GameStatistics: Object with min_turns, optimal_probability and combinations_without_looping.

    Raises:
        ValueError: If num_positions is less than 3.
    """
    _validate_board_size(num_positions)

    minimum_turns: int = (num_positions + 1) // 3

    optimal_paths: int = _calculate_paths_to_position(num_positions, minimum_turns)
    optimal_probability: float = optimal_paths / (3 ** minimum_turns)

    combinations_without_looping: int = _calculate_combinations_without_looping(num_positions)

    return GameStatistics(
        min_turns=minimum_turns,
        optimal_probability=optimal_probability,
        combinations_without_looping=combinations_without_looping
    )