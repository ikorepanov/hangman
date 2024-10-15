"""
Первая строка.

Этот модуль является основным скриптом приложения и отвечает за запуск
главной логики программы.
"""

import re
from pathlib import Path
from random import randrange

CWD = Path(__file__).parents[2]
DICT_PATH = CWD / 'data/dictionary.txt'

WELCOME_MESSAGE = """
 _____________________________________________________________
|                                                             |
|                                                             |
|              Вас приветствует игра "Виселица!               |
|                                                             |
|_____________________________________________________________|
"""

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
      __O    |
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

options = {
    '0': EMPTY,
    '1': HEAD,
    '2': BODY,
    '3': R_HAND,
    '4': L_HAND,
    '5': R_LEG,
    '6': L_LEG,
}


def get_random_word(default: str | None) -> str:
    """_summary_.

    :param default: _description_
    :type default: str | None
    :return: _description_
    :rtype: str
    """

    with DICT_PATH.open() as fhand:
        word = default
        for index, aline in enumerate(fhand, start=1):
            if randrange(index) == 0:
                word = aline
        if word is not None:
            return word.strip()
        return ''


def open_mask(
    mask: str,
    word: str,
    letter: str,
) -> str:
    """_summary_.

    :param mask: _description_
    :type mask: str
    :param word: _description_
    :type word: str
    :param letter: _description_
    :type letter: str
    :return: _description_
    :rtype: str
    """

    mask_asterisks = list(mask)
    indices = [index for index, char in enumerate(word) if char == letter]
    for index in indices:
        mask_asterisks[index] = letter
    return ''.join(mask_asterisks)


def build_hangman(mistakes: int) -> str:
    """_summary_.

    :param mistakes: _description_
    :type mistakes: int
    :return: _description_
    :rtype: str
    """

    action = options.get(str(mistakes))
    if action:
        return action
    return ''


def show_current_state(
    mask: str,
    mistakes: int,
) -> None:
    """_summary_.

    :param mask: _description_
    :type mask: str
    :param mistakes: _description_
    :type mistakes: int
    """

    print(
        ' '.join(mask),
        f'\n\nКоличество ошибок: {mistakes}\n',
        f'{build_hangman(mistakes)}',
    )


def not_cyrillic(letter: str) -> bool:
    """_summary_.

    :param letter: _description_
    :type letter: str
    :return: _description_
    :rtype: bool
    """

    if bool(not re.fullmatch('[ёа-я]', letter)):
        print(
            '\n\033[KНеобходимо использовать буквы',
            'русского алфавита: а - я (А - Я)',
            '\033[2F\033[K',
            end='',
        )
        return True
    return False


def already_used(
    used_letters: list[str],
    letter: str,
) -> bool:
    """_summary_.

    :param used_letters: _description_
    :type used_letters: list[str]
    :param letter: _description_
    :type letter: str
    :return: _description_
    :rtype: bool
    """

    if letter in used_letters:
        list_used_letters = ', '.join(used_letters)
        print(
            '\n\033[KВы уже вводили, в том числе, эту букву:',
            f'{list_used_letters}',
            '\033[2F\033[K',
            end='',
        )
        return True
    return False


def not_valid_symbol(
    used_letters: list[str],
    letter: str,
) -> bool:
    """_summary_.

    :param used_letters: _description_
    :type used_letters: list[str]
    :param letter: _description_
    :type letter: str
    :return: _description_
    :rtype: bool
    """

    return not_cyrillic(letter) or already_used(used_letters, letter)


def enter_letter(
    mask: str,
    mistakes: int,
    used_letters: list[str],
) -> str:
    """_summary_.

    :param mask: _description_
    :type mask: str
    :param mistakes: _description_
    :type mistakes: int
    :param used_letters: _description_
    :type used_letters: list[str]
    :return: _description_
    :rtype: str
    """
    show_current_state(mask, mistakes)

    while True:
        letter = input('Введите букву: ').lower()

        if not_valid_symbol(used_letters, letter):
            continue

        used_letters.append(letter)
        print('\033[12F\033[J', end='')

        return letter


def run_game(game_count: int) -> None:
    """_summary_.

    :param game_count: _description_
    :type game_count: int
    """

    if game_count == 0:
        print('\033[2F\033[J', end='')
    else:
        print('\033[16F\033[J', end='')

    word = get_random_word(default=None)

    mask = '*' * len(word)
    mistakes = 0
    used_letters: list[str] = []

    print('Отгадайте следующее слово:')

    while '*' in mask and mistakes < 6:
        letter = enter_letter(mask, mistakes, used_letters)

        if letter in word:
            mask = open_mask(mask, word, letter)
        else:
            mistakes += 1

    show_current_state(mask, mistakes)

    if mask == word:
        print('Поздравляем! Вы выиграли!\n')
    else:
        print('К сожалению, вы проиграли!\n')


def main() -> None:
    """_summary_."""

    print(WELCOME_MESSAGE)
    game_count = 0

    while True:
        decision = input('Начать новую игру (1) или выйти из приложения(2)? Введите 1 или 2:\n')

        if decision == '1':
            run_game(game_count)
            game_count += 1

        elif decision == '2':
            print('\033[K\033[EВсего доброго!\n')
            break

        else:
            print('(Нужно ввести 1 или 2)\033[F\033[K\033[F', end='')


if __name__ == '__main__':
    main()
