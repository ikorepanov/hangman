from pathlib import Path
from random import randrange

CWD = Path(__file__).parents[2]
DICT_PATH = CWD / 'data/dictionary.txt'


EMPTY = """
         ____
        |    |
             |
             |
             |
    _________|_____
"""
HEAD = """
         ____
        |    |
        O    |
             |
             |
    _________|_____
"""
BODY = """
         ____
        |    |
        O    |
        |    |
             |
    _________|_____
"""
R_HAND = """
         ____
        |    |
      __O    |
        |    |
             |
    _________|_____
"""
L_HAND = """
         ____
        |    |
      __O__  |
        |    |
             |
    _________|_____
"""
R_LEG = """
         ____
        |    |
      __O__  |
        |    |
       /     |
    _________|_____
"""
L_LEG = """
         ____
        |    |
      __O__  |
        |    |
       / \   |
    _________|_____
"""


def prepare_screen(game_count: int) -> None:
    if game_count == 0:
        print('\033[2F\033[J', end='')
    else:
        print('\033[16F\033[J', end='')


def get_random_word(default: str | None) -> str:
    with DICT_PATH.open() as fhand:
        word = default
        for index, aline in enumerate(fhand, start=1):
            if randrange(index) == 0:
                word = aline
        if word is not None:
            return word.strip()
        return ''


def init_start_params() -> tuple[str, str, int, list[str]]:
    word = get_random_word(default=None)
    mask = '*' * len(word)
    mistakes = 0
    used_letters: list[str] = []
    print('Отгадайте следующее слово:')
    return word, mask, mistakes, used_letters


def build_hangman(mistakes: int) -> str:
    stages = [
        EMPTY,
        HEAD,
        BODY,
        R_HAND,
        L_HAND,
        R_LEG,
        L_LEG,
    ]

    if 0 <= mistakes <= len(stages):
        return stages[mistakes]
    return ''


def show_current_state(
    mask: str,
    mistakes: int,
) -> None:
    print(
        ' '.join(mask),
        f'\n\nКоличество ошибок: {mistakes}\n',
        f'{build_hangman(mistakes)}',
    )


def open_mask(
    mask: str,
    word: str,
    letter: str,
) -> str:
    mask_asterisks = list(mask)
    indices = [index for index, char in enumerate(word) if char == letter]
    for index in indices:
        mask_asterisks[index] = letter
    return ''.join(mask_asterisks)


def process_letter(
    letter: str,
    word: str,
    mask: str,
    mistakes: int,
) -> tuple[str, int]:
    if letter in word:
        mask = open_mask(mask, word, letter)
    else:
        mistakes += 1
    print('\033[12F\033[J', end='')
    return mask, mistakes
