"""
Модуль для проверки и обработки пользовательского ввода в игре.

Этот модуль предоставляет функции для проверки корректности введённых букв,
а также для обработки повторяющихся или недопустимых символов в игре, где
используются кириллические символы.

Функции:
---------
- print_not_cyrillic: Выводит сообщение, если символ не является буквой русского алфавита.
- is_not_cyrillic: Проверяет, является ли символ кириллическим.
- print_already_used: Выводит список уже использованных букв.
- is_already_used: Проверяет, была ли буква уже введена ранее.
- is_not_valid_symbol: Проверяет, является ли символ недопустимым (не кириллическим или уже использованным).
- enter_letter: Запрашивает у пользователя ввод буквы и добавляет её в список использованных букв.
"""

import re


def print_not_cyrillic() -> None:
    """Выводит сообщение о необходимости использования букв русского алфавита.

    Функция отображает сообщение с указанием, что нужно использовать буквы
    русского алфавита от "а" до "я" (включая заглавные буквы).

    :return: None
    :rtype: None
    """

    print(
        '\n\033[KНеобходимо использовать буквы',
        'русского алфавита: а - я (А - Я)',
        '\033[2F\033[K',
        end='',
    )


def is_not_cyrillic(letter: str) -> bool:
    """Проверяет, является ли символ буквой русского алфавита.

    Если переданный символ не является буквой русского алфавита, выводится сообщение,
    и функция возвращает True.

    :param letter: Проверяемый символ
    :type letter: str
    :return: Возвращает True, если символ не кириллический, иначе False
    :rtype: bool
    """

    if bool(not re.fullmatch('[ёа-я]', letter)):
        print_not_cyrillic()
        return True
    return False


def print_already_used(used_letters: list[str]) -> None:
    """Выводит список уже введённых пользователем букв.

    Функция отображает сообщение, в котором перечислены буквы,
    которые пользователь уже вводил ранее.

    :param used_letters: Список букв, которые пользователь уже вводил
    :type used_letters: list[str]
    :return: None
    :rtype: None
    """

    list_used_letters = ', '.join(used_letters)
    print(
        '\n\033[KВы уже вводили, в том числе, эту букву:',
        f'{list_used_letters}',
        '\033[2F\033[K',
        end='',
    )


def is_already_used(
    used_letters: list[str],
    letter: str,
) -> bool:
    """Проверяет, была ли буква уже введена пользователем.

    Если буква была введена ранее, выводится сообщение со списком
    использованных букв, и функция возвращает True.

    :param used_letters: Список букв, которые пользователь уже вводил
    :type used_letters: list[str]
    :param letter: Проверяемая буква
    :type letter: str
    :return: Возвращает True, если буква уже была введена, иначе False
    :rtype: bool
    """

    if letter in used_letters:
        print_already_used(used_letters)
        return True
    return False


def is_not_valid_symbol(
    used_letters: list[str],
    letter: str,
) -> bool:
    """Проверяет, является ли символ недопустимым (не кириллическим или уже использованным).

    Функция объединяет две проверки: является ли символ буквой русского алфавита
    и была ли эта буква уже введена ранее.

    :param used_letters: Список букв, которые пользователь уже вводил
    :type used_letters: list[str]
    :param letter: Проверяемая буква
    :type letter: str
    :return:  Возвращает True, если символ недопустим, иначе False
    :rtype: bool
    """

    return is_not_cyrillic(letter) or is_already_used(used_letters, letter)


def enter_letter(used_letters: list[str]) -> str:
    """Запрашивает у пользователя ввод буквы.

    Функция запрашивает у пользователя ввод буквы, проверяет её допустимость и
    добавляет в список использованных букв.

    :param used_letters: Список букв, которые пользователь уже вводил
    :type used_letters: list[str]
    :return: Возвращает введённую пользователем допустимую букву
    :rtype: str
    """

    while True:
        letter = input('Введите букву: ').lower()
        if is_not_valid_symbol(used_letters, letter):
            continue
        used_letters.append(letter)
        return letter
