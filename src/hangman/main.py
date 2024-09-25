from random import randrange
import re 

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
    

class Hangman:
    def __init__(self):
        print(
            """
                 ____
                |    |
                     |
                     |
                     |
            _________|_____
            """
        )
    
    def add_head(self):
        print(
            """
                 ____
                |    |
                O    |
                     |
                     |
            _________|_____
            """
        )

    def add_body(self):
        print(
            """
                 ____
                |    |
                O    |
                |    |
                     |
            _________|_____
            """
        )

    def add_right_hand(self):
        print(
            """
                 ____
                |    |
              __O    |
                |    |
                     |
            _________|_____
            """
        )

    def add_left_hand(self):
        print(
            """
                 ____
                |    |
              __O__  |
                |    |
                     |
            _________|_____
            """
        )

    def add_right_leg(self):
        print(
            """
                 ____
                |    |
              __O__  |
                |    |
               /     |
            _________|_____
            """
        )

    def add_left_leg(self):
        print(
            """
                 ____
                |    |
              __O__  |
                |    |
               / \   |
            _________|_____
            """
        )


def is_cyrillic(char):
    return bool(re.fullmatch('[ёа-я]', char))


def main():
    with open('dictionary.txt') as f:
        word = get_random_word(f)
    
    mask = '*' * len(word)
    print(' '.join(mask))
    
    mistakes = 0
    print(build_hangman(mistakes))

    while '*' in mask and mistakes < 6:
        print(f'Количество ошибок: {mistakes}\n')
        
        while True:
            letter = input('Введи букву:\n')
            if is_cyrillic(letter):
                break
            else:
                print(
                    f'\nНеобходимо использовать - только - буквы '
                    f'русского алфавита в нижнем регистре: а - я\n'
                )
                continue

        if letter in word:
            indices = find_occurrences(word, letter)
            mask = open_mask(mask, letter, indices)
        else:
            mistakes += 1

        print(' '.join(mask))
        print(build_hangman(mistakes))
    
    if mask == word:
        print('\nCongrats!\n')
    else:
        print(f'Количество ошибок: {mistakes}')
        print('\nYou have just lost!\n')


while True:
    decision = input(
        'Начать новую игру или выйти из приложения? Введите "Y" или "N":\n'
    )
    if decision == 'Y':
        print(f'Вы ввели "{decision}". Начинаем!\nОтгадайте следующее слово\n')
        main()
    else: 
        print('Пока!')
        exit()
