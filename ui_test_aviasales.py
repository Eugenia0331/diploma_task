import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import allure
from config import MAIN_PAGE_URL

@pytest.mark.ui
@allure.story("UI")
@allure.title("Открытие главной страницы")
def test_open_main_page() -> None:
    driver = webdriver.Chrome()
    driver.maximize_window()
    try:
        with allure.step("Открываем главную страницу"):
            driver.get(MAIN_PAGE_URL)
        with allure.step("Проверяем, что логотип отображается"):
            logo = driver.find_element(By.CSS_SELECTOR, ".HeaderLogo")
            assert logo.is_displayed()
    finally:
        driver.quit()

@pytest.mark.ui
@allure.story("UI")
@allure.title("Проверка поиска билетов")
def test_ui_search_flights() -> None:
    driver = webdriver.Chrome()
    driver.maximize_window()
    try:
        with allure.step("Открываем главную страницу"):
            driver.get(MAIN_PAGE_URL)
        with allure.step("Вводим города Откуда и Куда"):
            driver.find_element(By.ID, "origin").send_keys("Москва")
            driver.find_element(By.ID, "destination").send_keys("Санкт-Петербург")
        with allure.step("Выбираем даты и нажимаем поиск"):
            driver.find_element(By.CSS_SELECTOR, ".SearchButton").click()
        with allure.step("Проверяем, что появились результаты"):
            results = driver.find_element(By.CSS_SELECTOR, ".TicketList")
            assert results.is_displayed()
    finally:
        driver.quit()

@pytest.mark.ui
@allure.story("UI")
@allure.title("Проверка пустого поиска")
def test_ui_empty_search() -> None:
    driver = webdriver.Chrome()
    driver.maximize_window()
    try:
        driver.get(MAIN_PAGE_URL)
        driver.find_element(By.CSS_SELECTOR, ".SearchButton").click()
        message = driver.find_element(By.CSS_SELECTOR, ".SearchError")
        assert message.is_displayed()
    finally:
        driver.quit()

@pytest.mark.ui
@allure.story("UI")
@allure.title("Проверка фильтрации по дате")
def test_ui_filter_by_date() -> None:
    driver = webdriver.Chrome()
    driver.maximize_window()
    try:
        driver.get(MAIN_PAGE_URL)
        # Вводим города
        driver.find_element(By.ID, "origin").send_keys("Москва")
        driver.find_element(By.ID, "destination").send_keys("Санкт-Петербург")
        # Выбираем дату
        driver.find_element(By.ID, "depart_date").send_keys("2025-12-20")
        driver.find_element(By.CSS_SELECTOR, ".SearchButton").click()
        # Проверяем фильтр
        date_elements = driver.find_elements(By.CSS_SELECTOR, ".TicketDate")
        assert all("20.12.2025" in el.text for el in date_elements)
    finally:
        driver.quit()

@pytest.mark.ui
@allure.story("UI")
@allure.title("Проверка сортировки по цене")
def test_ui_sort_by_price() -> None:
    driver = webdriver.Chrome()
    driver.maximize_window()
    try:
        driver.get(MAIN_PAGE_URL)
        driver.find_element(By.ID, "origin").send_keys("Москва")
        driver.find_element(By.ID, "destination").send_keys("Санкт-Петербург")
        driver.find_element(By.CSS_SELECTOR, ".SearchButton").click()
        # Применяем сортировку
        driver.find_element(By.CSS_SELECTOR, ".SortPrice").click()
        prices = [int(el.text.replace("₽","").replace(" ","")) for el in driver.find_elements(By.CSS_SELECTOR, ".TicketPrice")]
        assert prices == sorted(prices)
    finally:
        driver.quit()
