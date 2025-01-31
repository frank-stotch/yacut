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

Документация лежит в файле openapi.yml, который удобно читать в онлайн-редакторе [Swagger](https://editor.swagger.io/?url=https://raw.githubusercontent.com/frank-stotch/yacut/refs/heads/master/openapi.yml)

Техностек:
* Python
* Flask
* Flask-Migrate
* Flask-SQLAlchemy
* Flask-WTF
* SQLAlchemy

Автор: Иван Курилов [Frank_Stotch](https://github.com/frank-stotch)