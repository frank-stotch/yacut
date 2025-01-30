Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/frank-stotch/yacut.git
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

Для локального развёртывания сначала применить миграции, затем запустить приложение
```
flask db upgrade
```

```
flask run
```

Документация лежит в файле openapi.yml, который удобно читать в онлайн-редакторе [Swagger](https://editor.swagger.io/)

Техностек:
* Python 3.9
* Flask 3.0
* Flask-Migrate 4.0
* Flask-SQLAlchemy 3.1
* Flask-WTF 1.2
* SQLAlchemy 2.0

Автор: Иван Курилов [Frank_Stotch](https://github.com/frank-stotch)