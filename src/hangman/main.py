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


def get_random_word(default: str | None) -> str:
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
    mask_asterisks = list(mask)
    indices = [index for index, char in enumerate(word) if char == letter]
    for index in indices:
        mask_asterisks[index] = letter
    return ''.join(mask_asterisks)


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


def print_not_cyrillic() -> None:
    print(
        '\n\033[KНеобходимо использовать буквы',
        'русского алфавита: а - я (А - Я)',
        '\033[2F\033[K',
        end='',
    )


def not_cyrillic(letter: str) -> bool:
    if bool(not re.fullmatch('[ёа-я]', letter)):
        print_not_cyrillic()
        return True
    return False


def print_already_used(used_letters: list[str]) -> None:
    list_used_letters = ', '.join(used_letters)
    print(
        '\n\033[KВы уже вводили, в том числе, эту букву:',
        f'{list_used_letters}',
        '\033[2F\033[K',
        end='',
    )


def already_used(
    used_letters: list[str],
    letter: str,
) -> bool:
    if letter in used_letters:
        print_already_used(used_letters)
        return True
    return False


def not_valid_symbol(
    used_letters: list[str],
    letter: str,
) -> bool:
    return not_cyrillic(letter) or already_used(used_letters, letter)


def enter_letter(used_letters: list[str]) -> str:
    while True:
        letter = input('Введите букву: ').lower()
        if not_valid_symbol(used_letters, letter):
            continue
        used_letters.append(letter)
        return letter


def prepare_screen(game_count: int) -> None:
    if game_count == 0:
        print('\033[2F\033[J', end='')
    else:
        print('\033[16F\033[J', end='')


def print_final_message(
    mask: str,
    word: str,
) -> None:
    if mask == word:
        print('Поздравляем! Вы выиграли!\n')
    else:
        print('К сожалению, вы проиграли!\n')


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


def init_start_params() -> tuple[str, str, int, list[str]]:
    word = get_random_word(default=None)
    mask = '*' * len(word)
    mistakes = 0
    used_letters: list[str] = []
    print('Отгадайте следующее слово:')
    return word, mask, mistakes, used_letters


def run_game(game_count: int) -> None:
    prepare_screen(game_count)
    word, mask, mistakes, used_letters = init_start_params()

    while '*' in mask and mistakes < 6:
        show_current_state(mask, mistakes)
        letter = enter_letter(used_letters)
        mask, mistakes = process_letter(letter, word, mask, mistakes)

    show_current_state(mask, mistakes)
    print_final_message(mask, word)


def main() -> None:
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
