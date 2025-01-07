# Hangman

Первый проект роадмапа Сергея Жукова:
https://zhukovsd.github.io/python-backend-learning-course/

## Скриншоты

### Стартовый экран

![hangman1](https://github.com/user-attachments/assets/b8c1d6fa-dd89-4d52-8ecb-f815d13ae086)

### Начало игры

![hangman2](https://github.com/user-attachments/assets/009797a3-e371-43d5-8224-72edf069490f)

### Победа

![hangman3](https://github.com/user-attachments/assets/f38623c9-96de-4cee-867f-89762dd14d57)

## Установка

Клонируйте репозиторий:
```shell
git clone -b refactor/hangman-reviews https://github.com/ikorepanov/hangman.git
```

Перейдите в папку hangman:
```shell
cd hangman
```

Разверните виртуальное окружение:
```shell
python -m venv .venv
```

Активируйте виртуальное окружение:
* Linux и macOS
  ```shell
  source venv/bin/activate
  ```
* Windows
  ```shell
  source venv/Scripts/activate
  ```

Обновите `pip`:
```shell
python -m pip install --upgrade pip
```

Установите проект:
```shell
pip install .
```

## Использование

Запустите скрипт:
```shell
python src/hangman/main.py
```

или

```shell
python -m hangman.main
```

В дальнейшем - следуйте указаниям на экране.
