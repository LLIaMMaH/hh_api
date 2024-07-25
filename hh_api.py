import requests
import sqlite3
from colorama import init, Fore, Style
from datetime import datetime


class HeadHunterAPI:
    def __init__(self):
        self.base_url = "https://api.hh.ru"
        self.db_connection = sqlite3.connect('vacancies.db')
        self.create_table()

    def create_table(self):
        """Создание таблицы для хранения данных о вакансиях."""
        with self.db_connection:
            self.db_connection.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                id TEXT PRIMARY KEY,
                name TEXT,
                employer TEXT,
                area TEXT,
                published_at TEXT,
                salary_from REAL,
                salary_to REAL,
                currency TEXT,
                alternate_url TEXT,
                update_at TEXT
            )
            """)


    def search_vacancies(self, text, area=1, per_page=10):
        """Поиск вакансий по ключевым словам."""
        search_url = f"{self.base_url}/vacancies"
        params = {
            'text': text,
            'area': area,  # 1 - Москва, 2 - Санкт-Петербург и т.д.
            'per_page': per_page
        }
        response = requests.get(search_url, params=params)
        response.raise_for_status()  # Проверка на успешность запроса
        return response.json()

    def format_salary(self, salary_data):
        if salary_data is None:
            return 'Не указана'

        salary_from = salary_data.get('from', 0)
        salary_to = salary_data.get('to', 0)
        currency = salary_data.get('currency', '')
        if salary_from and salary_to:
            return f'От {salary_from} до {salary_to} {currency}'
        elif salary_from:
            return f'От {salary_from} {currency}'
        elif salary_to:
            return f'До {salary_to} {currency}'
        else:
            return 'Не указана'

    def print_vacancies(self, vacancies):
        """Вывод информации о вакансиях."""
        for item in vacancies['items']:
            print(f"{Fore.GREEN}Вакансия с id:{Style.RESET_ALL}: {Fore.YELLOW}{item['id']}")
            print(f"{Fore.GREEN}Название{Style.RESET_ALL}: {item['name']}")
            print(f"{Fore.GREEN}Компания{Style.RESET_ALL}: {item['employer']['name']}")
            print(f"{Fore.GREEN}Город{Style.RESET_ALL}: {item['area']['name']}")
            print(f"{Fore.GREEN}Опубликовано{Style.RESET_ALL}: {item['published_at']}")
            print(f"{Fore.GREEN}Заработная плата{Style.RESET_ALL}: {self.format_salary(item['salary'])}")
            print(f"{Fore.GREEN}Ссылка{Style.RESET_ALL}: {item['alternate_url']}")
            print("-" * 40)


if __name__ == "__main__":
    init(autoreset=True)
    hh_api = HeadHunterAPI()
    search_text = input(f"{Fore.CYAN}Введите ключевые слова для поиска вакансий{Style.RESET_ALL}: ")
    area_number = int(input(f"{Fore.CYAN}Регион (1 - Москва, 2 - Санкт-Петербург){Style.RESET_ALL}: "))
    ask_per_page = input(f"{Fore.CYAN}Сколько ваканций вывести (10 по умолчанию){Style.RESET_ALL}: ")
    per_page = 10
    if ask_per_page != "" and ask_per_page.isnumeric():
        per_page = int(ask_per_page)
    vacancies = hh_api.search_vacancies(search_text, area_number, per_page)
    hh_api.print_vacancies(vacancies)
