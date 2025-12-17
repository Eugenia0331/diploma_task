import pytest
import requests
import allure
from config import BASE_API_URL, MAIN_PAGE_URL

# =========================
# Позитивные API-тесты
# =========================

@pytest.mark.api
@allure.story("API")
@pytest.mark.parametrize(
    "from_city,to_city,depart_date,return_date,desc",
    [
        ("Москва", "Санкт-Петербург", "2025-12-20", "2025-12-25", "Поиск с кириллицей"),
        ("Moscow", "Saint-Petersburg", "2025-12-20", "2025-12-25", "Поиск с латиницей"),
        ("Москва", "Санкт-Петербург", "2025-12-20", "2025-12-20", "Одинаковые даты"),
        ("Москва", "Санкт-Петербург", "2025-12-22", "2025-12-28", "Разные даты"),
        ("Сочи", "Санкт-Петербург", "2025-12-22", "2025-12-29", "Разные города")
    ]
)
@allure.title("Проверка поиска билетов")
def test_search_flights_positive(from_city: str, to_city: str, depart_date: str, return_date: str, desc: str) -> None:
    with allure.step("Формируем запрос"):
        params = {
            "from": from_city,
            "to": to_city,
            "depart_date": depart_date,
            "return_date": return_date
        }
    with allure.step("Отправляем POST-запрос"):
        response = requests.post(BASE_API_URL, json=params)
    with allure.step("Проверяем статус-код и формат ответа"):
        assert response.status_code == 200, f"{desc}: Статус не 200"
        assert isinstance(response.json(), dict), f"{desc}: Ответ не JSON"

@pytest.mark.api
@allure.story("API")
@allure.title("Проверка главной страницы")
def test_main_page_status() -> None:
    with allure.step("Отправляем GET-запрос на главную страницу"):
        response = requests.get(MAIN_PAGE_URL)
    with allure.step("Проверяем статус-код"):
        assert response.status_code == 200

# =========================
# Негативные API-тесты
# =========================

@pytest.mark.api
@allure.story("API")
@allure.title("Негативный поиск GET вместо POST")
def test_search_with_get_method() -> None:
    params = {"from": "Москва", "to": "Санкт-Петербург", "depart_date": "2025-12-20", "return_date": "2025-12-25"}
    with allure.step("Отправляем GET-запрос"):
        response = requests.get(BASE_API_URL, params=params)
    with allure.step("Проверяем код ошибки 403"):
        assert response.status_code == 403

@pytest.mark.api
@allure.story("API")
@pytest.mark.parametrize(
    "from_city,to_city,depart_date,return_date,desc",
    [
        (None, None, None, None, "Пустой поиск"),
        ("Москва", "Москва", "2025-12-20", "2025-12-25", "Одинаковые пункты"),
        ("Москва", None, "2025-12-20", None, "Только пункт Откуда"),
        ("!@#$%", "^&*()", "2025-12-20", "2025-12-25", "Произвольные символы"),
        ("Сочи", "Сочи", "2025-12-22", "2025-12-22", "Тест с одинаковыми городами")
    ]
)
@allure.title("Негативный поиск с некорректными данными")
def test_search_invalid_inputs(from_city: str, to_city: str, depart_date: str, return_date: str, desc: str) -> None:
    with allure.step("Формируем запрос"):
        params = {}
        if from_city:
            params["from"] = from_city
        if to_city:
            params["to"] = to_city
        if depart_date:
            params["depart_date"] = depart_date
        if return_date:
            params["return_date"] = return_date
    with allure.step("Отправляем POST-запрос"):
        response = requests.post(BASE_API_URL, json=params)
    with allure.step("Проверяем статус-код"):
        assert response.status_code == 200, f"{desc}: Статус не 200"
