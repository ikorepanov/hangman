from pathlib import Path

from hangman.letter import enter_letter
from hangman.params import (
    CLEAR_SCREEN_FROM_HERE_TO_THE_END,
    DICT_PATH,
    REMEMBERING_THE_CURSOR_START_POSITION,
    RETURN_TO_THE_START_POSITION_OF_THE_CURSOR,
    STAGES,
    WELCOME_MESSAGE,
)
from hangman.tools import (
    init_start_params,
    process_letter,
    show_current_state,
)


def is_word_guessed(mask: list[str], word: str) -> bool:
    """Проверяет, отгадано ли слово."""

    return ''.join(mask) == word


def is_game_lost(mistakes: int, stages: list[str]) -> bool:
    """Проверяет, проиграна ли игра."""

    return mistakes == len(stages) - 1


def run_game(dict_path: Path, stages: list[str]) -> None:
    """Основной цикл игры "Виселица"."""

    print(REMEMBERING_THE_CURSOR_START_POSITION, end='')

    start_params = init_start_params(dict_path)

    word = start_params['word']
    mask = start_params['mask']
    mistakes = start_params['mistakes']
    used_letters = start_params['used_letters']

    show_current_state(mask, mistakes, stages)

    while True:
        letter = enter_letter(used_letters)

        print(RETURN_TO_THE_START_POSITION_OF_THE_CURSOR, end='')
        print(CLEAR_SCREEN_FROM_HERE_TO_THE_END, end='')

        mask, mistakes = process_letter(letter, word, mask, mistakes)

        show_current_state(mask, mistakes, stages)

        if is_word_guessed(mask, word):
            print('Поздравляем! Вы выиграли!\n')
            break

        if is_game_lost(mistakes, stages):
            print(f'К сожалению, вы проиграли! Было загадано слово "{word}"\n')
            break


def main() -> None:
    """Основная функция, запускающая приложение."""

    print(WELCOME_MESSAGE)
    print(REMEMBERING_THE_CURSOR_START_POSITION, end='')

    dict_path = DICT_PATH
    stages = STAGES

    while True:
        decision = input('Начать новую игру (1) или выйти из приложения(2)? Введите 1 или 2:\n')

        if decision == '1':
            print(RETURN_TO_THE_START_POSITION_OF_THE_CURSOR, end='')
            print(CLEAR_SCREEN_FROM_HERE_TO_THE_END, end='')
            run_game(dict_path, stages)

        elif decision == '2':
            print(CLEAR_SCREEN_FROM_HERE_TO_THE_END, end='')
            print()
            print('Всего доброго!')
            print()
            break

        else:
            print('(Нужно ввести 1 или 2)')
            print(RETURN_TO_THE_START_POSITION_OF_THE_CURSOR, end='')


if __name__ == '__main__':
    main()
