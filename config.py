import os

# Основные настройки
BASE_API_URL: str = os.getenv("BASE_API_URL", "https://www.aviasales.ru/api/search")
MAIN_PAGE_URL: str = os.getenv("MAIN_PAGE_URL", "https://www.aviasales.ru/?params=LON1")
