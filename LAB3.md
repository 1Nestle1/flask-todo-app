# Лабораторная работа 3: CI для Flask

Workflow: `.github/workflows/ci-native.yml`.

При push в master, pull request в master или ручном запуске GitHub Actions:
1. Разворачивает Ubuntu и Python 3.12.
2. Устанавливает зависимости и проверяет их совместимость (`pip check`).
3. Проверяет синтаксис Python (`compileall`).
4. Проверяет полный цикл работы с задачей в изолированной SQLite-базе.
5. Удаляет базу только в одноразовом CI-окружении и применяет миграцию (`flask db upgrade`).
6. Запускает Flask на 127.0.0.1:7345 и проверяет HTTP 200 и содержимое страницы через curl. Лог сервера выводится и при ошибке.

## Локальный запуск

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m flask --app manage:app db upgrade
python manage.py runserver
```

Открыть http://127.0.0.1:7345/.

Исходный проект использовал Python 2 и Flask 0.11. Обновлены импорты, print, сортировка SQLAlchemy и зависимости; Flask-Script заменён встроенным Flask CLI. Оформление приложения сохранено.

## Проверка результата на GitHub

Откройте Actions → Flask native CI → последний запуск → validate-and-smoke → Smoke test Flask server.
В логе успешного запуска должны быть `HTTP/1.1 200 OK` и `Smoke test passed: Flask returned HTTP 200 and the TODO page.`
