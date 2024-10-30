# Hangman

Первый проект роадмапа Сергея Жукова:
https://zhukovsd.github.io/python-backend-learning-course/

## Установка

В проекте, для управления зависимостями, используется pdm:
https://pdm-project.org/en/latest/

Если не установлен, устанавливаем pdm:
```shell
pip install --user pdm
```

Клонируем репозиторий:
```shell
git clone https://github.com/ikorepanov/hangman.git
cd hangman
```

Создаём и активируем ВО:
```shell
python -m venv .venv
source .venv/bin/activate
```

Устанавливаем зависимости:
```shell
pdm install
```

## Использование

Запускаем скрипт:
```shell
python src/hangman/main.py
```

или

```shell
python -m src.hangman.main
```

В дальнейшем - следуем указаниям на экране.
