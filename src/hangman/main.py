from random import randrange
import re
from pathlib import Path


def get_random_word(fhand, default=None):
    word = default
    for i, aline in enumerate(fhand, start=1):
        if randrange(i) == 0:
            word = aline
    return word.strip()


def find_occurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]


def open_mask(mask, letter, indices):
    letters = list(mask)
    for index in indices:
        letters[index] = letter
    mask = ''.join(letters)
    return mask


def build_hangman(mistakes):
    if mistakes == 0:
        return """
             ____
            |    |
                 |
                 |
                 |
        _________|_____
        """
    elif mistakes == 1:
        return """
             ____
            |    |
            O    |
                 |
                 |
        _________|_____
        """
    elif mistakes == 2:
        return """
             ____
            |    |
            O    |
            |    |
                 |
        _________|_____
        """
    elif mistakes == 3:
        return """
             ____
            |    |
          __O    |
            |    |
                 |
        _________|_____
        """
    elif mistakes == 4:
        return """
             ____
            |    |
          __O__  |
            |    |
                 |
        _________|_____
        """
    elif mistakes == 5:
        return """
             ____
            |    |
          __O__  |
            |    |
           /     |
        _________|_____
        """
    elif mistakes == 6:
        return """
             ____
            |    |
          __O__  |
            |    |
           / \   |
        _________|_____
        """
    

def is_cyrillic(char):
    return bool(re.fullmatch('[ёа-я]', char))


def first_time(letters, letter):
    if letter not in letters:
        return True
    else:
        return False


def print_welcome_message():
    print(
            ' __________________________________________________________________\n'
            '|                                                                  |\n'
            '|                                                                  |\n'
            '|                  Вас приветствует игра "Виселица!                |\n'
            '|                                                                  |\n'
            '|__________________________________________________________________|\n'
        )


def ask_for_user_descision():
    return input(
        'Начать новую игру или выйти из приложения? Введите "Y" или "N":\n'
    )


def show_current_state(mask, mistakes):
    print(
        ' '.join(mask),
        '\n\n'
        f'Количество ошибок: {mistakes}\n'
        f'{build_hangman(mistakes)}'
    )

print_welcome_message()
game_count = 0

while True:
    decision = ask_for_user_descision()

    if decision == 'Y':

        if game_count == 0:
            print('\033[F' * 3, end='')
            print('\033[J', end='')
        else:
            print('\033[F' * 17, end='')
            print('\033[J', end='')

        CWD = Path(__file__).parents[2]
        path = CWD / 'data/dictionary.txt'
        with path.open() as f:
            word = get_random_word(f)
        
        mask = '*' * len(word)

        print('\nОтгадайте следующее слово:')
        
        mistakes = 0
        used_letters = []
        
        while '*' in mask and mistakes < 6:
            show_current_state(mask, mistakes)
            
            while True:
                letter = input('Введи букву: ')

                if letter == 'Стоп':
                    print('\033[K', end='')
                    print('\nВы решили закончить игру. Всего доброго!\n')
                    exit()

                elif not is_cyrillic(letter):
                    print(
                        f'\nНеобходимо использовать - только - буквы '
                        f'русского алфавита в нижнем регистре: а - я\n'
                    )
                    print('\033[F\033[F\033[F\033[F\033[K', end='')
                    continue

                elif not first_time(used_letters, letter):
                    print(
                        f'\nВы уже вводили, в том числе, эту букву: '
                        f'{", ".join(used_letters)}\n'
                    )
                    print('\033[F\033[F\033[F\033[F\033[K', end='')
                    continue

                else:
                    used_letters.append(letter)
                    print('\033[F' * 12, end='')
                    print('\033[J', end='')
                    break
        
            if letter in word:
                indices = find_occurrences(word, letter)
                mask = open_mask(mask, letter, indices)
            else:
                mistakes += 1

        show_current_state(mask, mistakes) 

        if mask == word:
            print('Congrats!\n')
        else:
            print('You have just lost!\n')
    
        game_count += 1

    else:
        print('\033[F' * 2, end='')
        print('\033[J', end='')
        print('Пока!\n')
        exit()
