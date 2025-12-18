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
        ("Москва", "Санкт-Петербург", "2025-12-20", "2025-12-25", "Кириллица"),
        ("Moscow", "Saint-Petersburg", "2025-12-20", "2025-12-25", "Латиница"),
        ("Москва", "Санкт-Петербург", "2025-12-20", "2025-12-20", "Одинаковые даты"),
    ]
)
@allure.title("POST /api/search без авторизации возвращает 403")
def test_search_post_requires_auth(
    from_city: str,
    to_city: str,
    depart_date: str,
    return_date: str,
    desc: str
) -> None:
    with allure.step("Формируем тело запроса"):
        payload = {
            "from": from_city,
            "to": to_city,
            "depart_date": depart_date,
            "return_date": return_date
        }

    with allure.step("Отправляем POST-запрос без авторизации"):
        response = requests.post(BASE_API_URL, json=payload)

    with allure.step("Проверяем, что доступ запрещён"):
        assert response.status_code == 403, f"{desc}: API должно требовать авторизацию"


@pytest.mark.api
@allure.story("API")
@allure.title("GET /api/search возвращает 404")
def test_search_with_get_method_returns_404() -> None:
    params = {
        "from": "Москва",
        "to": "Санкт-Петербург",
        "depart_date": "2025-12-20",
        "return_date": "2025-12-25"
    }

    with allure.step("Отправляем GET-запрос"):
        response = requests.get(BASE_API_URL, params=params)

    with allure.step("Проверяем, что эндпоинт недоступен по GET"):
        assert response.status_code == 404


# =========================
# Негативные API-тесты
# =========================

@pytest.mark.api
@allure.story("API")
@pytest.mark.parametrize(
    "payload,desc",
    [
        ({}, "Пустое тело"),
        ({"from": "Москва"}, "Только пункт отправления"),
        ({"from": "Москва", "to": "Москва"}, "Одинаковые города"),
        ({"from": "!@#$%", "to": "^&*()"}, "Некорректные символы"),
    ]
)
@allure.title("POST /api/search с некорректными данными возвращает 403")
def test_search_invalid_payloads(payload: dict, desc: str) -> None:
    with allure.step("Отправляем POST-запрос без авторизации"):
        response = requests.post(BASE_API_URL, json=payload)

    with allure.step("Проверяем запрет доступа"):
        assert response.status_code == 403, f"{desc}: API должно быть закрыто"
        

