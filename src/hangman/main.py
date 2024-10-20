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
    if mask == word:
        print('Поздравляем! Вы выиграли!\n')
    else:
        print('К сожалению, вы проиграли!\n')


def run_game(game_count: int) -> None:
    prepare_screen(game_count)
    word, mask, mistakes, used_letters = init_start_params()

    while '*' in mask and mistakes < 6:
        show_current_state(mask, mistakes)
        letter = enter_letter(used_letters)
        mask, mistakes = process_letter(letter, word, mask, mistakes)

    show_current_state(mask, mistakes)
    print_final_message(mask, word)


def main() -> None:
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
