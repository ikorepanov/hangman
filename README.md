# Hangman

Первый проект роадмапа Сергея Жукова:
https://zhukovsd.github.io/python-backend-learning-course/

## Скриншоты

### Стартовый экран

![start](https://github.com/user-attachments/assets/fa9ad5c4-82f5-420b-bd62-de59d2ac0344)

### Начало игры

![beginning](https://github.com/user-attachments/assets/1ee1cbf8-ac1e-4dbc-9b4c-75929edcd562)

### Победа

![win](https://github.com/user-attachments/assets/f75fd6fb-0d69-4f35-8b59-eb8f0d4ef4ec)

### Поражение

![lost](https://github.com/user-attachments/assets/0e494378-a9ec-4e7a-aa8a-706d6de8a9a8)

### Предупреждение

![warn](https://github.com/user-attachments/assets/abad2ab8-8022-481f-b66a-874f1541ec83)

### Завершение

![bye](https://github.com/user-attachments/assets/7602bdb8-6152-4016-a2db-98baf68721b1)

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
  source .venv/bin/activate
  ```
* Windows
  ```shell
  source .venv/Scripts/activate
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

Запустите приложение:
```shell
python -m hangman.main
```

В дальнейшем - следуйте указаниям на экране.
