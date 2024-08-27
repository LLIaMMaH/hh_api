# -*- coding: utf-8 -*-

from colorama import init, Fore, Style
from environs import Env
from utils.api_connector import HeadHunterAPI
from utils.database_manager import DatabaseManager

init(autoreset=True)
env = Env()
env.read_env()

CLIENT_ID = env.str('CLIENT_ID')
CLIENT_SECRET = env.str('CLIENT_SECRET')
REDIRECT_URI = env.str('REDIRECT_URI')

db_manager = DatabaseManager()
hh_api = HeadHunterAPI(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, db_manager)


def main():
    hh_api.authenticate()
    search_text = input(f"{Fore.CYAN}Введите ключевые слова:{Style.RESET_ALL} ")
    area_number = int(input(f"{Fore.CYAN}Регион (1 - Москва, 2 - СПб){Style.RESET_ALL}: "))
    ask_per_page = input(f"{Fore.CYAN}Сколько вакансий вывести (10 по умолчанию){Style.RESET_ALL}: ")
    per_page = 10
    if ask_per_page != "" and ask_per_page.isnumeric():
        per_page = int(ask_per_page)
        if per_page > 100:
            per_page = 100
            print(f"{Fore.RED}Максимально допустимое значение 100")
    vacancies = hh_api.search_vacancies(search_text, area_number, per_page)
    hh_api.print_vacancies(vacancies)
    db_manager.process_vacancies(vacancies)


if __name__ == "__main__":
    main()