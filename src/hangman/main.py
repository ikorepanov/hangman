import re
from pathlib import Path
from random import randrange
from typing import Any

from hangman.params import (
    CLEAR_SCREEN_TO_END,
    DICT_PATH,
    RESTORE_CURSOR_POSITION,
    SAVE_CURSOR_POSITION,
    STAGES,
    WELCOME_MESSAGE,
)


def is_cyrillic(letter: str) -> bool:
    """Проверяет, является ли символ буквой русского алфавита."""

    return bool(re.fullmatch('[ёа-я]', letter))


def is_already_used(
    letter: str,
    used_letters: list[str],
) -> bool:
    """Проверяет, была ли буква уже введена пользователем."""

    return letter in used_letters


def validate_letter(
    letter: str,
    used_letters: list[str],
) -> tuple[bool, str]:
    """Проверяет, является ли введённая буква валидной."""

    if not is_cyrillic(letter):
        return False, 'Необходимо использовать буквы русского алфавита: а - я (А - Я)'

    if is_already_used(letter, used_letters):
        return False, 'Вы уже вводили эту букву (см. Использованные буквы)'

    return True, ''


def enter_letter(used_letters: list[str]) -> str:
    """Запрашивает ввод буквы, проверяет её допустимость и добавляет в список использованных букв."""

    while True:
        letter = input('Введите букву: ').lower()

        is_valid, error_message = validate_letter(letter, used_letters)

        if not is_valid:
            print(f'\n\033[K{error_message}\033[2F\033[K', end='')
            continue

        used_letters.append(letter)

        return letter


def get_random_word(
    dict_path: Path,
    default: str = 'виселица',
) -> str:
    """Возвращает случайное слово из файла словаря, или значение по умолчанию, если файл пуст или не существует."""

    try:
        with dict_path.open('r', encoding='UTF-8') as fhand:
            word = default
            line_count = 0

            for index, line in enumerate(fhand, start=1):
                line_count += 1
                # С вероятностью 1/index выбираем текущее слово
                if randrange(index) == 0:
                    word = line.strip()

            if line_count == 0:  # Если файл пуст
                print(f'Файл {dict_path} пуст. Используется слово по умолчанию.')
                return default

            return word

    except FileNotFoundError:
        print(f'Файл {dict_path} не найден. Используется слово по умолчанию.')
        return default


def init_start_params(dict_path: Path) -> dict[str, Any]:
    """Инициализирует стартовые параметры игры и возвращает их в виде словаря."""

    start_params: dict[str, Any] = {}
    word = get_random_word(dict_path)

    start_params['word'] = word
    start_params['mask'] = ['_'] * len(word)
    start_params['mistakes'] = 0
    start_params['used_letters'] = []

    return start_params


def build_hangman(
    mistakes: int,
    stages: list[str],
) -> str:
    """Возвращает текущую сцену виселицы в зависимости от числа ошибок."""

    if 0 <= mistakes <= len(stages) - 1:
        return stages[mistakes]
    return ''


def show_current_state(
    mask: str,
    mistakes: int,
    used_letters: list[str],
    stages: list[str],
) -> None:
    """Отображает текущее состояние маски слова, количество ошибок, состояние виселицы и использованные буквы."""

    print(f'{" ".join(mask)}\n\n')
    print(f'Количество ошибок: {mistakes}')
    print(f'{build_hangman(mistakes, stages)}\n')
    print(f'Использованные буквы: {", ".join(used_letters)}\n')


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


def send_ansi(sequence: str) -> None:
    """Отправляет ANSI-последовательность в терминал."""

    print(sequence, end='')


def run_game(
    dict_path: Path,
    stages: list[str],
) -> None:
    """Основной цикл игры "Виселица"."""

    send_ansi(SAVE_CURSOR_POSITION)

    start_params = init_start_params(dict_path)

    word = start_params['word']
    mask = start_params['mask']
    mistakes = start_params['mistakes']
    used_letters = start_params['used_letters']

    show_current_state(mask, mistakes, used_letters, stages)

    while True:
        letter = enter_letter(used_letters)

        send_ansi(RESTORE_CURSOR_POSITION)
        send_ansi(CLEAR_SCREEN_TO_END)

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
        decision = input('Начать новую игру (1) или выйти из приложения(2)? Введите 1 или 2:\n')

        if decision == '1':
            send_ansi(RESTORE_CURSOR_POSITION)
            send_ansi(CLEAR_SCREEN_TO_END)
            run_game(dict_path, stages)

        elif decision == '2':
            send_ansi(CLEAR_SCREEN_TO_END)
            print()
            print('Всего доброго!')
            print()
            break

        else:
            print('(Нужно ввести 1 или 2)')
            send_ansi(RESTORE_CURSOR_POSITION)


if __name__ == '__main__':
    main()
