def escape_curly_braces(text: str) -> str:
    """
    Escape curly braces in the given text.

    :param text: The text to escape.
    :return:     The text with the curly braces escaped.
    """
    return text.replace("{", "{{").replace("}", "}}")
