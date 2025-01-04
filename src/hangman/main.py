import re
import sys
from pathlib import Path
from random import randrange
from typing import Any

from hangman.params import (
    CLEAR_CURRENT_LINE,
    CLEAR_SCREEN_TO_END,
    CYRILLIC_LETTER_MSG,
    DICT_PATH,
    EMPTY_LINE_MSG,
    RESTORE_CURSOR_POSITION,
    SAVE_CURSOR_POSITION,
    STAGES,
    USED_LETTER_MSG,
    WELCOME_MESSAGE,
)


def is_empty_line(letter: str) -> bool:
    """Проверяет, ввёл ли пользователь пустую строку."""

    return letter == ''


def is_cyrillic(letter: str) -> bool:
    """Проверяет, является ли символ буквой русского алфавита."""

    return bool(re.fullmatch('[ёа-я]', letter))


def is_already_used(
    letter: str,
    used_letters: list[str],
) -> bool:
    """Проверяет, была ли буква уже введена пользователем."""

    return letter in used_letters


class ValidationResult:
    def __init__(
        self,
        is_valid: bool,
        message: str = '',
    ):
        self.is_valid = is_valid
        self.message = message


def validate_letter(
    letter: str,
    used_letters: list[str],
) -> ValidationResult:
    """Проверяет, является ли введённая буква валидной."""

    if is_empty_line(letter):
        return ValidationResult(False, EMPTY_LINE_MSG)

    if not is_cyrillic(letter):
        return ValidationResult(False, CYRILLIC_LETTER_MSG)

    if is_already_used(letter, used_letters):
        return ValidationResult(False, USED_LETTER_MSG.format(letter))

    return ValidationResult(True)


def move_cursor_up(lines: int) -> str:
    """Возвращает ANSI-код для перемещения курсора вверх на указанное количество строк."""

    return f'\033[{lines}F'


def send_ansi(sequence: str) -> None:
    """Отправляет ANSI-последовательность в терминал."""

    print(sequence, end='')


def restore_cursor_and_clear_screen() -> None:
    """Отправляет в терминал ANSI-коды для возврата курсора в запомненную позицию и очистки экрана."""

    send_ansi(RESTORE_CURSOR_POSITION)
    send_ansi(CLEAR_SCREEN_TO_END)


def display_error_and_retry(error_message: str) -> None:
    print()
    send_ansi(CLEAR_CURRENT_LINE)
    print(error_message)
    send_ansi(move_cursor_up(3))
    send_ansi(CLEAR_CURRENT_LINE)


def enter_letter(used_letters: list[str]) -> str:
    """Запрашивает ввод буквы, проверяет её допустимость и добавляет в список использованных букв."""

    while True:
        letter = input('Введите букву: ').lower()

        if len(letter) > 1:
            letter = letter[0]

        result = validate_letter(letter, used_letters)

        if not result.is_valid:
            display_error_and_retry(result.message)
            continue

        used_letters.append(letter)

        return letter


class DictionaryFileError(Exception):
    """Кастомное исключение для ошибок, связанных с обработкой файла."""

    pass


def get_random_word(dict_path: Path) -> str:
    """Возвращает случайное слово из файла."""

    if not dict_path.exists():
        raise DictionaryFileError(f'Файл {dict_path} не найден.\n')

    with dict_path.open('r', encoding='UTF-8') as fhand:
        word = None

        for index, line in enumerate(fhand, start=1):
            if randrange(0, index) == 0:
                word = line.strip()

        if word is None:
            raise DictionaryFileError(f'Файл {dict_path} пуст.\n')

        return word


def init_start_params(dict_path: Path) -> dict[str, Any]:
    """Инициализирует стартовые параметры игры и возвращает их в виде словаря."""

    try:
        word = get_random_word(dict_path)
    except DictionaryFileError:
        raise

    return {
        'word': word,
        'mask': ['_'] * len(word),
        'mistakes': 0,
        'used_letters': []
    }


def build_hangman(
    mistakes: int,
    stages: list[str],
) -> str:
    """Возвращает текущую сцену виселицы в зависимости от числа ошибок."""

    if 0 <= mistakes <= len(stages) - 1:
        return stages[mistakes]
    return ''


def format_current_state(
    mask: str,
    mistakes: int,
    used_letters: list[str],
    stages: list[str]
) -> str:
    """Формирует набор данных для отображения текущего состояния."""

    return (
        f'{" ".join(mask)}\n'
        f'{build_hangman(mistakes, stages)}\n\n'
        f'Количество ошибок: {mistakes}\n\n'
        f'Использованные буквы: {", ".join(used_letters)}\n'
    )


def show_current_state(
    mask: str,
    mistakes: int,
    used_letters: list[str],
    stages: list[str],
) -> None:
    """Отображает текущее состояние маски слова, количество ошибок, состояние виселицы и использованные буквы."""

    print(format_current_state(mask, mistakes, used_letters, stages))


def open_mask(
    mask: list[str],
    word: str,
    letter: str,
) -> list[str]:
    """Открывает в маске все вхождения угаданной буквы."""

    for index, char in enumerate(word):
        if char == letter:
            mask[index] = letter
    return mask


def process_letter(
    letter: str,
    word: str,
    mask: list[str],
    mistakes: int,
) -> tuple[list[str], int]:
    """Обрабатывает введённую пользователем букву."""

    if letter in word:
        mask = open_mask(mask, word, letter)
    else:
        mistakes += 1

    return mask, mistakes


def is_word_guessed(
    mask: list[str],
    word: str,
) -> bool:
    """Проверяет, отгадано ли слово."""

    return ''.join(mask) == word


def is_game_lost(
    mistakes: int,
    stages: list[str],
) -> bool:
    """Проверяет, проиграна ли игра."""

    return mistakes == len(stages) - 1


def run_game(
    dict_path: Path,
    stages: list[str],
) -> None:
    """Основной цикл игры "Виселица"."""

    send_ansi(SAVE_CURSOR_POSITION)

    try:
        start_params = init_start_params(dict_path)
    except DictionaryFileError:
        raise

    word = start_params['word']
    mask = start_params['mask']
    mistakes = start_params['mistakes']
    used_letters = start_params['used_letters']

    show_current_state(mask, mistakes, used_letters, stages)

    while True:
        letter = enter_letter(used_letters)
        restore_cursor_and_clear_screen()
        mask, mistakes = process_letter(letter, word, mask, mistakes)
        show_current_state(mask, mistakes, used_letters, stages)

        if is_word_guessed(mask, word):
            print('Поздравляем! Вы выиграли!\n')
            break

        if is_game_lost(mistakes, stages):
            print(f'К сожалению, вы проиграли! Было загадано слово "{word}"\n')
            break


def main() -> None:
    """Основная функция, запускающая приложение."""

    print(WELCOME_MESSAGE)
    send_ansi(SAVE_CURSOR_POSITION)

    dict_path = DICT_PATH
    stages = STAGES

    while True:
        decision = input('Начать новую игру (1) или выйти из приложения (2)?\n\nВведите 1 или 2: ')

        if decision == '1':
            restore_cursor_and_clear_screen()
            try:
                run_game(dict_path, stages)
            except DictionaryFileError as error:
                print(error)
                sys.exit(1)

        elif decision == '2':
            send_ansi(CLEAR_SCREEN_TO_END)
            print()
            print('Всего доброго!\n')
            break

        else:
            print()
            print(f'Нужно ввести 1 или 2. Вы ввели "{decision}"')
            send_ansi(move_cursor_up(3))
            send_ansi(CLEAR_CURRENT_LINE)
            send_ansi(move_cursor_up(2))


if __name__ == '__main__':
    main()
