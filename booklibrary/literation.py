import re


def transliterate(text):
    """
    Transliterates a string from one language to another.

    Args:
        text (str): The string to transliterate.

    Returns:
        str: The transliterated string.
    """

    # Create a dictionary of transliteration rules.
    transliteration_rules = {
        'а': 'a',
        'б': 'b',
        'в': 'v',
        'г': 'g',
        'д': 'd',
        'е': 'e',
        'ж': 'zh',
        'з': 'z',
        'и': 'i',
        'к': 'k',
        'л': 'l',
        'м': 'm',
        'н': 'n',
        'о': 'o',
        'п': 'p',
        'р': 'r',
        'с': 's',
        'т': 't',
        'у': 'u',
        'ф': 'f',
        'х': 'h',
        'ы': 'y',
        'ь': '\'',
        'щ': 'shch',
        'ч': 'ch',
        'ш': 'sh',
        'ю': 'iu',
        'я': 'ya',
    }

    # Transliterate the string.
    transliterated_text = ''
    for char in text:
        if char in transliteration_rules:
            transliterated_text += transliteration_rules[char]
        else:
            transliterated_text += char

    # Return the transliterated string.
    return transliterated_text


def re_transliterate(text):
    """
    Transliterates a string from one language to another.

    Args:
        text (str): The string to re-transliterate.

    Returns:
        str: The transliterated string.
    """

    # Create a dictionary of transliteration rules.
    transliteration_rules = {
        'a': 'а',
        'b': 'б',
        'v': 'в',
        'g': 'г',
        'd': 'д',
        'e': 'е',
        'z': 'з',
        'i': 'и',
        'j': 'й',
        'k': 'к',
        'l': 'л',
        'm': 'м',
        'n': 'н',
        'o': 'о',
        'p': 'п',
        'r': 'р',
        's': 'с',
        't': 'т',
        'u': 'у',
        'f': 'ф',
        'h': 'х',
        'y': 'ы',
        '\'': 'ь',
        'zh': 'ж',
        'shch': 'щ',
        'ch': 'ч',
        'sh': 'ш',
        'iu': 'ю',
        'yu': 'ю',
        'ya': 'я',
        'ja': 'я',
    }

    # Transliterate the string.
    transliterated_text = ''
    tmp_text = text
    while len(tmp_text) > 0:
        literal1, literal2, literal4 = get_literals_set(tmp_text)
        if literal4 in transliteration_rules:
            tmp_text = tmp_text[4:]
            transliterated_text += transliteration_rules.get(literal4)
            continue
        if literal2 in transliteration_rules:
            tmp_text = tmp_text[2:]
            transliterated_text += transliteration_rules.get(literal2)
            continue
        tmp_text = tmp_text[1:]
        transliterated_text += transliteration_rules.get(literal1, literal1)

    # Return the transliterated string.
    return transliterated_text


def get_literals_set(text):
    return get_next_literal(text, 1), get_next_literal(text, 2), get_next_literal(text, 4)


def get_next_literal(text, base=1):
    if len(text) >= base:
        return text[:base].lower()
    return ''


def detect_russian_letters(string):
    """
    Checks if the given string contains Russian letters.

    Args:
        string: The string to check.

    Returns:
        True if Russian letters are detected, False otherwise.
    """

    regex = r"[\u0400-\u04FF]"
    return bool(re.search(regex, string))
