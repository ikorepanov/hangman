import re


def print_not_cyrillic() -> None:
    print(
        '\n\033[KНеобходимо использовать буквы',
        'русского алфавита: а - я (А - Я)',
        '\033[2F\033[K',
        end='',
    )


def is_not_cyrillic(letter: str) -> bool:
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


def is_already_used(
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
    return is_not_cyrillic(letter) or is_already_used(used_letters, letter)


def enter_letter(used_letters: list[str]) -> str:
    while True:
        letter = input('Введите букву: ').lower()
        if not_valid_symbol(used_letters, letter):
            continue
        used_letters.append(letter)
        return letter
