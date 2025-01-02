from pathlib import Path

CWD = Path(__file__).parents[2]
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
L_LEG = """
         ____
        |    |
      __O__  |
        |    |
       / \   |
    _________|_____
"""

STAGES = [EMPTY, HEAD, BODY, R_HAND, L_HAND, R_LEG, L_LEG]

SAVE_CURSOR_POSITION = '\033[s'
RESTORE_CURSOR_POSITION = '\033[u'
CLEAR_SCREEN_TO_END = '\033[J'
CLEAR_CURRENT_LINE = '\033[K'
