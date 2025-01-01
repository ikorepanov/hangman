from pathlib import Path
from random import randrange
from typing import Any


def prepare_screen(game_count: int) -> None:
    """Подготавливает экран для новой игры.

    Если это первая игра, поднимает курсор на 2 строки вверх и очищает экран,
    в противном случае поднимает курсор на 16 строк вверх и очищает предыдущие выводы.

    :param game_count: Количество уже сыгранных игр
    :type game_count: int
    :return: None
    :rtype: None
    """

    if game_count == 0:
        print('\033[2F\033[J', end='')
    else:
        print('\033[16F\033[J', end='')


def get_random_word(dict_path: Path, default: str = 'виселица') -> str:
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
    start_params['mask'] = ['*'] * len(word)
    start_params['mistakes'] = 0
    start_params['used_letters'] = []

    return start_params


def build_hangman(mistakes: int, stages: list[str]) -> str:
    """Возвращает текущую сцену виселицы в зависимости от числа ошибок."""

    if 0 <= mistakes <= len(stages) - 1:
        return stages[mistakes]
    return ''


def show_current_state(
    mask: str,
    mistakes: int,
    stages: list[str],
) -> None:
    """Отображает текущее состояние маски слова и количество ошибок.

    Выводит на экран текущую маску слова с угаданными буквами и количество
    сделанных ошибок, а также соответствующую сцену виселицы.

    :param mask: Текущая маска слова (с угаданными буквами)
    :type mask: str
    :param mistakes: Количество сделанных ошибок
    :type mistakes: int
    :return: None
    :rtype: None
    """

    print(
        ' '.join(mask),
        f'\n\nКоличество ошибок: {mistakes}\n',
        f'{build_hangman(mistakes, stages)}',
    )


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
