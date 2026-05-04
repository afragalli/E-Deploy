from constants.errors import ERROR_POSITION_LESS_THAN_ONE

def _validate_position(position: int) -> None:
    """
    Validates if the position is valid for 1-indexed sequences.

    Args:
        position (int): The position to be validated.

    Raises:
        ValueError: If the position is less than 1, using ERROR_POSITION_LESS_THAN_ONE.
    """
    if position < 1:
        raise ValueError(ERROR_POSITION_LESS_THAN_ONE)

def get_sequence_value(position: int) -> int:
    """
    Calculates the value of a number at a specific position in an arithmetic progression.

    The sequence (11, 18, 25, 32, 39...) has an initial term a1 = 11
    and a common difference r = 7. The formula used is a_n = a1 + (position - 1) * r.

    Args:
        position (int): The desired position in the sequence (1-indexed).

    Returns:
        int: The numeric value corresponding to the informed position.

    Raises:
        ValueError: If the position is less than 1, using ERROR_POSITION_LESS_THAN_ONE.
    """
    _validate_position(position)

    return 11 + (position - 1) * 7