from pathlib import Path

from hangman.letter import enter_letter
from hangman.params import (
    DICT_PATH,
    STAGES,
    WELCOME_MESSAGE,
)
from hangman.tools import (
    init_start_params,
    prepare_screen,
    process_letter,
    show_current_state,
)


def print_final_message(
    mask: list[str],
    word: str,
) -> None:
    """Выводит сообщение о победе или поражении в игре."""

    if ''.join(mask) == word:
        print('Поздравляем! Вы выиграли!\n')
    else:
        print(f'К сожалению, вы проиграли! Было загадано слово "{word}"\n')


def run_game(game_count: int, dict_path: Path, stages: list[str]) -> None:
    """Основной цикл игры "Виселица".

    Инициализирует параметры игры, управляет процессом угадывания букв и выводит текущее состояние игры.
    Игра продолжается, пока игрок не отгадает слово или не наберет 6 ошибок.
    """

    prepare_screen(game_count)
    start_params = init_start_params(dict_path)

    word = start_params['word']
    mask = start_params['mask']
    mistakes = start_params['mistakes']
    used_letters = start_params['used_letters']

    while ''.join(mask) != word and mistakes < len(stages) - 1:
        show_current_state(mask, mistakes, stages)
        letter = enter_letter(used_letters)
        mask, mistakes = process_letter(letter, word, mask, mistakes)

    show_current_state(mask, mistakes, stages)
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
    dict_path = DICT_PATH
    stages = STAGES

    while True:
        decision = input('Начать новую игру (1) или выйти из приложения(2)? Введите 1 или 2:\n')

        if decision == '1':
            run_game(game_count, dict_path, stages)
            game_count += 1

        elif decision == '2':
            print('\033[K\033[EВсего доброго!\n')
            break

        else:
            print('(Нужно ввести 1 или 2)\033[F\033[K\033[F', end='')


if __name__ == '__main__':
    main()
