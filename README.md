### О проекте

Проект укорачиватель ссылок. Длинная ссылка сокращается до короткой.

### Технологический стек

Python 3.9, Flask 2.0.2, SQLAlchemy 1.4.29

### Автор

Никита Сергеевич Федяев

Telegram: [@nsfed](https://t.me/nsfed)

Репозиторий: [GitHub](git@github.com:Fedoska48/yacut.git)

Клонировать репозиторий и перейти в него в командной строке:

```
git clone 
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Предварительно перед запуском необходимо запонить файл .env:

FLASK_APP=yacut

SQLALCHEMY_DATABASE_URI=*путь к БД*

А также прописать SECRET_KEY

Для работы в дебаг режиме необходимо указать FLASK_DEBUG=True

* Запустить проект можно командой в терминале:

```
flask run
```

Спецификация к API в файле:

**openapi.yml**