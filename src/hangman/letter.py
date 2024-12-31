import re


def is_cyrillic_letter(letter: str) -> bool:
    """Проверяет, является ли символ буквой русского алфавита."""

    return bool(re.fullmatch('[ёа-я]', letter))


def is_already_used(
    letter: str,
    used_letters: list[str],
) -> bool:
    """Проверяет, была ли буква уже введена пользователем."""

    return letter in used_letters


def validate_letter(letter: str, used_letters: list[str]) -> tuple[bool, str]:
    """Проверяет, является ли введённая буква валидной."""

    if not is_cyrillic_letter(letter):
        return False, 'Необходимо использовать буквы русского алфавита: а - я (А - Я)'
    if is_already_used(letter, used_letters):
        list_used_letters = ', '.join(used_letters)
        return False, f'Вы уже вводили, в том числе, эту букву: {list_used_letters}'
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
