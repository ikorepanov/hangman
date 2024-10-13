import re
from random import randrange

from paths import DICT_PATH

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


def get_random_word(
    default: str | None,
) -> str:
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
    action = options.get(str(mistakes))
    if action:
        return action
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


def enter_letter(
    mask: str,
    mistakes: int,
    used_letters: list[str],
) -> str:
    show_current_state(mask, mistakes)

    while True:
        letter = input('Введите букву: ')

        if bool(not re.fullmatch('[ёа-я]', letter)):
            print(
                '\nНеобходимо использовать - только - буквы',
                'русского алфавита в нижнем регистре: а - я',
                '\033[2F\033[K',
                end='',
            )
            continue

        elif letter in used_letters:
            list_used_letters = ', '.join(used_letters)
            print(
                '\nВы уже вводили, в том числе, эту букву:',
                f'{list_used_letters}',
                '\033[2F\033[K',
                end='',
            )
            continue

        used_letters.append(letter)
        print('\033[12F\033[J', end='')

        return letter


def run_game(game_count: int) -> None:
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
