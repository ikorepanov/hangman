import re
import sys
from pathlib import Path
from random import randrange
from typing import Any, NamedTuple

from hangman.params import (
    CLEAR_CURRENT_LINE,
    CLEAR_SCREEN_TO_END,
    CYRILLIC_LETTER_MSG,
    DICT_PATH,
    EMPTY_LINE_MSG,
    MORE_THAN_ONE_SYMBOL_MSK,
    STAGES,
    USED_LETTER_MSG,
    WELCOME_MESSAGE,
)

from hangman.tools import get_cursor_pos, GettingCursorPos


def move_cursor_to(x: str, y: str) -> str:
    return f'\033[{y};{x}H'


def send_ansi(sequence: str) -> None:
    """Отправляет ANSI-последовательность в терминал."""

    print(sequence, end='')


def restore_cursor_and_clear_screen(x: str, y: str) -> None:
    """Отправляет в терминал ANSI-коды для возврата курсора в запомненную позицию и очистки экрана."""

    send_ansi(move_cursor_to(x, y))
    send_ansi(CLEAR_SCREEN_TO_END)


def show_warning_and_retry(error_message: str, x: str, y: str) -> None:
    """Перемещает курсор, стирая не нужное и печатая сообщение."""

    print()
    send_ansi(CLEAR_CURRENT_LINE)
    print(error_message, end='')
    send_ansi(move_cursor_to(x, y))
    send_ansi(CLEAR_CURRENT_LINE)


class ValidationResult(NamedTuple):
    is_positive: bool
    message: str = ''


def validate_letter(
    letter: str,
    used_letters: list[str],
) -> ValidationResult:
    """Проверяет, является ли введённая буква валидной."""

    if not letter:
        return ValidationResult(False, EMPTY_LINE_MSG)

    if len(letter) > 1:
        return ValidationResult(False, MORE_THAN_ONE_SYMBOL_MSK)

    if not re.fullmatch('[ёа-я]', letter):
        return ValidationResult(False, CYRILLIC_LETTER_MSG)

    if letter in used_letters:
        return ValidationResult(False, USED_LETTER_MSG.format(letter))

    return ValidationResult(True)


def enter_letter(used_letters: list[str]) -> str:
    """Запрашивает ввод буквы, проверяет её допустимость и добавляет в список использованных букв."""

    entering_letter_pos = get_cursor_pos()

    while True:
        letter = input('Введите букву: ').lower()

        result_of_letter_validation = validate_letter(letter, used_letters)

        if not result_of_letter_validation.is_positive:
            show_warning_and_retry(result_of_letter_validation.message, entering_letter_pos.x, entering_letter_pos.y)
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
            line = line.strip()
            if not line:
                continue
            if randrange(0, index) == 0:
                word = line

        if word is None:
            raise DictionaryFileError(f'Файл {dict_path} пуст.\n')

        return word


def init_start_params(dict_path: Path) -> dict[str, Any]:
    """Инициализирует стартовые параметры игры и возвращает их в виде словаря."""

    word = get_random_word(dict_path)

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
    mask: list[str],
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


def render_game_state(
    mask: list[str],
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


class ProcessingResult(NamedTuple):
    mask: list[str]
    mistakes: int


def process_letter(
    letter: str,
    word: str,
    mask: list[str],
    mistakes: int,
) -> ProcessingResult:
    """Обрабатывает введённую пользователем букву."""

    if letter in word:
        mask = open_mask(mask, word, letter)
    else:
        mistakes += 1

    return ProcessingResult(mask, mistakes)


def run_game(
    dict_path: Path,
    stages: list[str],
    start_pos: GettingCursorPos,
) -> None:
    """Основной цикл игры "Виселица"."""

    start_params = init_start_params(dict_path)

    word = start_params['word']
    mask = start_params['mask']
    mistakes = start_params['mistakes']
    used_letters = start_params['used_letters']

    render_game_state(mask, mistakes, used_letters, stages)

    while True:
        letter = enter_letter(used_letters)
        result_of_letter_processing = process_letter(letter, word, mask, mistakes)

        mask = result_of_letter_processing.mask
        mistakes = result_of_letter_processing.mistakes
        restore_cursor_and_clear_screen(start_pos.x, start_pos.y)
        render_game_state(mask, mistakes, used_letters, stages)

        if ''.join(mask) == word:
            print('Поздравляем! Вы выиграли!\n')
            break

        if mistakes == len(stages) - 1:
            print(f'К сожалению, вы проиграли! Было загадано слово "{word}"\n')
            break


def get_user_decision(start_pos: GettingCursorPos) -> str:
    """Принимает от пользователя решение о продолжении игры."""

    while True:
        decision = input('Начать новую игру (1) или выйти из приложения (2)? ')

        if decision in {'1', '2'}:
            return decision

        show_warning_and_retry(f'Нужно ввести 1 или 2. Вы ввели "{decision}"', start_pos.x, start_pos.y)
        send_ansi(move_cursor_to(start_pos.x, start_pos.y))


def main() -> None:
    """Основная функция."""

    print(WELCOME_MESSAGE)
    initial_cursor_position = get_cursor_pos()

    while True:
        decision = get_user_decision(initial_cursor_position)

        if decision == '2':  # Выход
            send_ansi(CLEAR_SCREEN_TO_END)
            print('\nВсего доброго!\n')
            break

        restore_cursor_and_clear_screen(initial_cursor_position.x, initial_cursor_position.y)

        try:
            run_game(DICT_PATH, STAGES, initial_cursor_position)
        except DictionaryFileError as error:
            print(error)
            sys.exit(1)


if __name__ == '__main__':
    main()
