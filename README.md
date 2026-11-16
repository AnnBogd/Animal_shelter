**Проект приюта для животных Animal Shelter.**

*Этот сайт для тех, кто хочет найти себе питомца.*
*Выбирай друга, оставь заявку на знакомство - и совсем скоро счастливых историй станет больше.*

Стек технологий: Python 3.12, Django, HTML, Bootstrap, SQLite.

Запуск проекта:

1. Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:AnnBogd/Animal_shelter.git
```
```
cd Animal_shelter
```

2. Создать и активировать виртуальное окружение (ОС Windows)
```
python -m vevn venv
source venv/Scripts/activate
```

3. Установить зависимости:
```
pip install -r requirements
```

4. Создать миграции
```
python manage.py makemigrations
```

5. Применить миграции
```
python manage.py migrate
```

6. Запуск проекта:
```
python manage.py runserver
```
