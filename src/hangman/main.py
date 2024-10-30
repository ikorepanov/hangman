"""
Модуль для запуска игры "Виселица".

Этот модуль управляет циклом игры, отображает приветственное сообщение, 
обрабатывает ввод пользователя для начала новой игры или выхода, 
и определяет, выиграл ли игрок.

Константы:
-----------
- WELCOME_MESSAGE: Приветственное сообщение, выводимое при запуске игры.

Функции:
---------
- print_final_message: Выводит финальное сообщение о результате игры (победа или поражение).
- run_game: Основной игровой цикл, который инициализирует параметры, управляет состоянием игры и обрабатывает ходы.
- main: Основная функция, отображающая приветственное сообщение и предлагающая начать новую игру или выйти из приложения.
"""

from hangman.letter import enter_letter
from hangman.tools import (
    init_start_params,
    prepare_screen,
    process_letter,
    show_current_state,
)

WELCOME_MESSAGE = """
 _____________________________________________________________
|                                                             |
|                                                             |
|              Вас приветствует игра "Виселица!               |
|                                                             |
|_____________________________________________________________|
"""


def print_final_message(
    mask: str,
    word: str,
) -> None:
    """Выводит финальное сообщение о результате игры.

    Если маска совпадает с загаданным словом, выводит сообщение о победе.
    В противном случае выводит сообщение о поражении.

    :param mask: Текущая маска слова (с угаданными буквами)
    :type mask: str
    :param word: Загаданное слово
    :type word: str
    :return: None
    :rtype: None
    """

    if mask == word:
        print('Поздравляем! Вы выиграли!\n')
    else:
        print('К сожалению, вы проиграли!\n')


def run_game(game_count: int) -> None:
    """Основной цикл игры "Виселица".

    Инициализирует параметры игры (слово, маску, ошибки, использованные буквы),
    управляет процессом угадывания букв и выводит текущее состояние игры.
    Игра продолжается, пока игрок не отгадает слово или не наберет 6 ошибок.

    :param game_count: Количество сыгранных игр для управления экраном
    :type game_count: int
    :return: None
    :rtype: None
    """

    prepare_screen(game_count)
    word, mask, mistakes, used_letters = init_start_params()

    while '*' in mask and mistakes < 6:
        show_current_state(mask, mistakes)
        letter = enter_letter(used_letters)
        mask, mistakes = process_letter(letter, word, mask, mistakes)

    show_current_state(mask, mistakes)
    print_final_message(mask, word)


def main() -> None:
    """Основная функция, запускающая приложение.

    Выводит приветственное сообщение и предлагает пользователю выбрать:
    начать новую игру или выйти из приложения. Запускает новую игру при выборе 1
    или завершает приложение при выборе 2.

    :return: None
    :rtype: None
    """

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
