import re
from io import TextIOWrapper
from random import randrange

from paths import DICT_PATH


def get_random_word(
        fhand: TextIOWrapper,
        default: str | None,
) -> str:
    word = default
    for i, aline in enumerate(fhand, start=1):
        if randrange(i) == 0:
            word = aline
    if word is not None:
        return word.strip()
    else:
        return ''


def open_mask(
        mask: str,
        word: str,
        letter: str,
) -> str:
    mask_asterisks = list(mask)
    indices = [i for i, char in enumerate(word) if char == letter]
    for index in indices:
        mask_asterisks[index] = letter
    return ''.join(mask_asterisks)


def build_hangman(mistakes: int) -> str:
    if mistakes == 0:
        return """
             ____
            |    |
                 |
                 |
                 |
        _________|_____
        """
    elif mistakes == 1:
        return """
             ____
            |    |
            O    |
                 |
                 |
        _________|_____
        """
    elif mistakes == 2:
        return """
             ____
            |    |
            O    |
            |    |
                 |
        _________|_____
        """
    elif mistakes == 3:
        return """
             ____
            |    |
          __O    |
            |    |
                 |
        _________|_____
        """
    elif mistakes == 4:
        return """
             ____
            |    |
          __O__  |
            |    |
                 |
        _________|_____
        """
    elif mistakes == 5:
        return """
             ____
            |    |
          __O__  |
            |    |
           /     |
        _________|_____
        """
    elif mistakes == 6:
        return """
             ____
            |    |
          __O__  |
            |    |
           / \\   |
        _________|_____
        """
    else:
        return ''


def is_cyrillic(char: str) -> bool:
    return bool(re.fullmatch('[ёа-я]', char))


def first_time(
        letters: list[str],
        letter: str,
) -> bool:
    if letter not in letters:
        return True
    else:
        return False


def print_welcome_message() -> None:
    print(
            ' _____________________________________________________________\n'
            '|                                                             |\n'
            '|                                                             |\n'
            '|              Вас приветствует игра "Виселица!               |\n'
            '|                                                             |\n'
            '|_____________________________________________________________|\n'
        )


def show_current_state(
        mask: str,
        mistakes: int,
) -> None:
    print(
        ' '.join(mask),
        '\n\n'
        f'Количество ошибок: {mistakes}\n'
        f'{build_hangman(mistakes)}'
    )


def enter_letter(
        mask: str,
        mistakes: int,
        used_letters: list[str],
) -> str:
    show_current_state(mask, mistakes)

    while True:
        letter = input('Введите букву: ')
        if not is_cyrillic(letter):
            print(
                '\nНеобходимо использовать - только - буквы',
                'русского алфавита в нижнем регистре: а - я',
                '\033[2F\033[K',
                end='',
            )
            continue
        elif not first_time(used_letters, letter):
            print(
                '\nВы уже вводили, в том числе, эту букву:',
                f'{", ".join(used_letters)}',
                '\033[2F\033[K',
                end='',
            )
            continue
        else:
            used_letters.append(letter)
            print('\033[12F\033[J', end='')
            return letter


def prepare_screen(game_count: int) -> None:
    if game_count == 0:
        print('\033[2F\033[J', end='')
    else:
        print('\033[16F\033[J', end='')


def run_game(game_count: int) -> None:
    prepare_screen(game_count)

    with DICT_PATH.open() as f:
        word = get_random_word(f, default=None)

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
    print_welcome_message()
    game_count = 0

    while True:
        decision = input(
            'Начать новую игру (1) или выйти из приложения(2)? '
            'Введите 1 или 2:\n'
        )

        if decision == '1':
            run_game(game_count)
            game_count += 1

        elif decision == '2':
            print('\033[K\033[EВсего доброго!\n')
            exit()

        else:
            print('(Нужно ввести 1 или 2)\033[F\033[K\033[F', end='')


if __name__ == '__main__':
    main()
