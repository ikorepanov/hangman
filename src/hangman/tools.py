# Источник:
# https://stackoverflow.com/questions/35526014/how-can-i-get-the-cursors-position-in-an-ansi-terminal

import re
import sys
from typing import NamedTuple

if (sys.platform == "win32"):
    import ctypes
    from ctypes import wintypes  # noqa: F401
else:
    import termios


class GettingCursorPos(NamedTuple):
    """Хранит координаты курсора в виде строковых значений."""

    x: str
    y: str


class TerminalError(Exception):
    """Исключение, связанное с ошибками работы терминала."""

    pass


def get_cursor_pos() -> GettingCursorPos:
    """Получает текущую позицию курсора в терминале."""

    if (sys.platform == "win32"):
        OldStdinMode = ctypes.wintypes.DWORD()
        OldStdoutMode = ctypes.wintypes.DWORD()
        kernel32 = ctypes.windll.kernel32
        kernel32.GetConsoleMode(kernel32.GetStdHandle(-10), ctypes.byref(OldStdinMode))
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), 0)
        kernel32.GetConsoleMode(kernel32.GetStdHandle(-11), ctypes.byref(OldStdoutMode))
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

    else:
        OldStdinMode = termios.tcgetattr(sys.stdin)
        _ = termios.tcgetattr(sys.stdin)
        _[3] = _[3] & ~(termios.ECHO | termios.ICANON)
        termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, _)

    try:
        _ = ""
        sys.stdout.write("\x1b[6n")
        sys.stdout.flush()
        while not (_ := _ + sys.stdin.read(1)).endswith('R'):
            True
        res = re.match(r".*\[(?P<y>\d*);(?P<x>\d*)R", _)

    finally:
        if (sys.platform == "win32"):
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-10), OldStdinMode)
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), OldStdoutMode)
        else:
            termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, OldStdinMode)

    if (res):
        x = res.group("x")
        y = res.group("y")
        return GettingCursorPos(x, y)

    raise TerminalError(
        'Во время выполнения программы возникла ошибка, связанная с несовместимостью с терминалом.'
        'Возможно, ваш терминал не поддерживает ANSI escape-коды. '
        'Попробуйте использовать другой терминал или операционную систему.'
    )
