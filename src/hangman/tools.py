"""
Модуль для управления состояниями игры "Виселица".

Этот модуль предоставляет функции для инициализации игры, обработки ходов,
построения виселицы в зависимости от количества ошибок и отображения текущего
состояния игры.

Константы:
-----------
- EMPTY, HEAD, BODY, R_HAND, L_HAND, R_LEG, L_LEG: Сцены для построения виселицы на каждом этапе ошибок.

Функции:
---------
- prepare_screen: Подготавливает экран для начала новой игры.
- get_random_word: Возвращает случайное слово из файла словаря.
- init_start_params: Инициализирует параметры игры (слово, маска, ошибки, использованные буквы).
- build_hangman: Возвращает текущее состояние виселицы на основе количества ошибок.
- show_current_state: Показывает текущее состояние маски слова, количество ошибок и виселицу.
- open_mask: Открывает буквы в маске, если они угаданы.
- process_letter: Обрабатывает введённую букву, обновляя маску или увеличивая количество ошибок.
"""

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


def get_random_word(default: str | None) -> str:
    """Возвращает случайное слово из файла словаря.

    Читает файл словаря и выбирает случайное слово. Если файл пуст, возвращает
    заданное значение по умолчанию.

    :param default: Значение по умолчанию, если не удалось выбрать слово
    :type default: str | None
    :return: Случайное слово из словаря
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


def init_start_params() -> tuple[str, str, int, list[str]]:
    """Инициализирует стартовые параметры игры.

    Возвращает случайное слово, его маску (скрытые буквы), начальное количество
    ошибок и пустой список использованных букв.

    :return: Кортеж из слова, маски, количества ошибок и использованных букв
    :rtype: tuple[str, str, int, list[str]]
    """

    word = get_random_word(default=None)
    mask = '*' * len(word)
    mistakes = 0
    used_letters: list[str] = []
    print('Отгадайте следующее слово:')
    return word, mask, mistakes, used_letters


def build_hangman(mistakes: int) -> str:
    """Возвращает текущее состояние виселицы в зависимости от количества ошибок.

    :param mistakes: Количество сделанных ошибок
    :type mistakes: int
    :return: Сцена виселицы, соответствующая текущему количеству ошибок
    :rtype: str
    """

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
        f'{build_hangman(mistakes)}',
    )


def open_mask(
    mask: str,
    word: str,
    letter: str,
) -> str:
    """Открывает угаданные буквы в маске.

    Функция обновляет маску, открывая все вхождения угаданной буквы.

    :param mask: Текущая маска слова
    :type mask: str
    :param word: Загаданное слово
    :type word: str
    :param letter: Угаданная буква
    :type letter: str
    :return: Обновлённая маска с открытыми буквами
    :rtype: str
    """

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
    """Обрабатывает введённую пользователем букву.

    Если буква угадана, обновляет маску, в противном случае увеличивает
    количество ошибок.

    :param letter: Введённая пользователем буква
    :type letter: str
    :param word: Загаданное словао
    :type word: str
    :param mask: Текущая маска слова
    :type mask: str
    :param mistakes: Количество сделанных ошибок
    :type mistakes: int
    :return: Обновлённая маска и количество ошибок
    :rtype: tuple[str, int]
    """

    if letter in word:
        mask = open_mask(mask, word, letter)
    else:
        mistakes += 1
    print('\033[12F\033[J', end='')
    return mask, mistakes
