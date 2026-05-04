def check_b_a_pattern(text: str) -> bool:
    """
    Checks if a string starts with the letter 'B' and ends with the letter 'A'.

    The verification is case-sensitive.

    Args:
        text (str): The string to be checked.

    Returns:
        bool: True if the string meets the criteria, False otherwise.
    """
    return text.startswith('B') and text.endswith('A')