from pathlib import Path

if '__file__' not in globals():
    raise RuntimeError('Переменная __file__ не определена')

path = Path(__file__)
if len(path.parents) < 3:
    raise ValueError('Недостаточно уровней в пути для доступа к parents[2]')

CWD = path.parents[2]
DICT_PATH = CWD / 'data/dictionary.txt'

WELCOME_MESSAGE = """
 _____________________________________________________________
|                                                             |
|              Вас приветствует игра "Виселица!               |
|                                                             |
|               Отгадайте зашифрованное слово                 |
|_____________________________________________________________|
"""

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
L_LEG = r"""
         ____
        |    |
      __O__  |
        |    |
       / \   |
    _________|_____
"""

STAGES = [EMPTY, HEAD, BODY, R_HAND, L_HAND, R_LEG, L_LEG]

CLEAR_SCREEN_TO_END = '\033[J'
CLEAR_CURRENT_LINE = '\033[K'

CYRILLIC_LETTER_MSG = 'Необходимо использовать буквы русского алфавита: а - я (А - Я)'
USED_LETTER_MSG = 'Вы уже вводили букву "{}" (см. Использованные буквы)'
EMPTY_LINE_MSG = 'Вы отправляете пустую строку. Введите букву'
MORE_THAN_ONE_SYMBOL_MSG = 'Вы ввели более одного символа. Введите один'
