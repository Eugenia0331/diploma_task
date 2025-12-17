# Автоматизированное тестирование Aviasales

## Описание проекта
Проект содержит автоматизированные UI и API тесты для платформы Aviasales.

## Структура проекта
- `test/api/` — API тесты
- `test/ui/` — UI тесты
- `config.py` — конфигурация (URL, токены)
- `requirements.txt` — зависимости
- `README.md` — инструкции

## Установка
```bash
git clone <URL_репозитория>
cd aviasales_test_project
pip install -r requirements.txt

## Запуск тестов

   pytest -v  - # все тесты

   pytest -v -m "api" - # только API

   pytest -v -m "ui" - # только UI

## Отчеты в Allure

  pytest --alluredir=allure-results
  allure serve allure-results
