import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import MAIN_PAGE_URL

# Фикстура браузера

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

# Тест 1. Открытие главной страницы (логотип)

@pytest.mark.ui
@allure.story("UI")
@allure.title("Открытие главной страницы")
def test_open_main_page(driver) -> None:
    with allure.step("Открываем главную страницу"):
        driver.get(MAIN_PAGE_URL)

    with allure.step("Проверяем, что логотип отображается"):
        logo = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="header-logo"]')
            )
        )
        assert logo.is_displayed()

# Тест 2. Поиск авиабилетов

@pytest.mark.ui
@allure.story("UI")
@allure.title("Проверка поиска билетов")
def test_ui_search_flights(driver) -> None:
    driver.get(MAIN_PAGE_URL)

    with allure.step("Вводим города Откуда и Куда"):
        origin = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[placeholder="Откуда"]'))
        )
        origin.send_keys("Москва")
        origin.send_keys(Keys.ENTER)

        destination = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Куда"]')
        destination.send_keys("Санкт-Петербург")
        destination.send_keys(Keys.ENTER)

    with allure.step("Нажимаем поиск"):
        search_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="form-submit"]')
        search_button.click()

    with allure.step("Проверяем, что появились результаты"):
        results = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '[data-testid="ticket"]')
            )
        )
        assert results is not None

# Тест 3. Пустой поиск

@pytest.mark.ui
@allure.story("UI")
@allure.title("Проверка пустого поиска")
def test_ui_empty_search(driver) -> None:
    driver.get(MAIN_PAGE_URL)

    driver.find_element(By.CSS_SELECTOR, '[data-testid="form-submit"]').click()

    error = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.CSS_SELECTOR, '[data-testid="origin-error"]')
        )
    )
    assert error.is_displayed()

# Тест 4. Фильтрация по дате

@pytest.mark.ui
@allure.story("UI")
@allure.title("Проверка фильтрации по дате")
def test_ui_filter_by_date(driver) -> None:
    driver.get(MAIN_PAGE_URL)

    origin = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[placeholder="Откуда"]'))
    )
    origin.send_keys("Москва", Keys.ENTER)

    destination = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Куда"]')
    destination.send_keys("Санкт-Петербург", Keys.ENTER)

    # Выбор даты (пример: первая доступная)
    driver.find_element(By.CSS_SELECTOR, '[data-testid="date-input"]').click()
    driver.find_element(By.CSS_SELECTOR, '[data-testid="calendar-day"]').click()

    driver.find_element(By.CSS_SELECTOR, '[data-testid="form-submit"]').click()

    tickets = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, '[data-testid="ticket"]')
        )
    )
    assert len(tickets) > 0

# Тест 5. Сортировка по цене

@pytest.mark.ui
@allure.story("UI")
@allure.title("Проверка сортировки по цене")
def test_ui_sort_by_price(driver) -> None:
    driver.get(MAIN_PAGE_URL)

    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Откуда"]').send_keys("Москва", Keys.ENTER)
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Куда"]').send_keys("Санкт-Петербург", Keys.ENTER)

    driver.find_element(By.CSS_SELECTOR, '[data-testid="form-submit"]').click()

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="ticket"]'))
    )

    driver.find_element(By.CSS_SELECTOR, '[data-testid="sort-by-price"]').click()

    prices = [
        int(el.text.replace("₽", "").replace(" ", ""))
        for el in driver.find_elements(By.CSS_SELECTOR, '[data-testid="ticket-price"]')
    ]

    assert prices == sorted(prices)



