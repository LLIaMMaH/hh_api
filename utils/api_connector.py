# -*- coding: utf-8 -*-

import datetime
import requests
from colorama import Fore, Style


class HeadHunterAPI:
    def __init__(self, client_id, client_secret, redirect_uri, db_manager):
        self.base_url = "https://api.hh.ru"
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.token = None
        self.db_manager = db_manager

    def authenticate(self):
        """Аутентификация и получение токена, если нет действующего токена."""
        token, expires_in, created_at = self.db_manager.get_token()

        if token:
            self.token = token
            print(f"{Fore.GREEN}Используем сохраненный токен, действующий до {created_at + datetime.timedelta(seconds=expires_in)}{Style.RESET_ALL}")
        else:
            auth_url = f"{self.base_url}/token"
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            data = {
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
            }
            try:
                response = requests.post(auth_url, headers=headers, data=data)
                response.raise_for_status()
                response_data = response.json()
                self.token = response_data.get('access_token')
                expires_in = response_data.get('expires_in')
                print(f"{Fore.GREEN}Получен новый токен, действительный {expires_in} секунд.{Style.RESET_ALL}")
                print(response_data)
                self.db_manager.save_token(self.token, expires_in)
            except requests.exceptions.HTTPError as err:
                print(f"{Fore.RED}Ошибка HTTP: {err}{Style.RESET_ALL}")
                print(f"{Fore.RED}Контент ответа: {response.text}{Style.RESET_ALL}")
                raise

    def search_vacancies(self, text, area=1, per_page=10):
        if not self.token:
            raise Exception("Authentication required")
        search_url = f"{self.base_url}/vacancies"
        headers = {'Authorization': f'Bearer {self.token}'}
        params = {'text': text, 'area': area, 'per_page': per_page}
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def format_salary(self, salary_data) -> str:
        """Приводим зарплату к одной строке."""
        if salary_data is None:
            return 'Не указана'

        salary_from = salary_data.get('from', 0)
        salary_to = salary_data.get('to', 0)
        currency = salary_data.get('currency', '')
        gross = salary_data.get('gross', False)
        gross_string = ''
        if gross:
            gross_string = ' до вычета налогов'
        if salary_from and salary_to:
            return f'От {salary_from} до {salary_to} {currency}{gross_string}'
        elif salary_from:
            return f'От {salary_from} {currency}{gross_string}'
        elif salary_to:
            return f'До {salary_to} {currency}{gross_string}'
        else:
            return 'Не указана'

    def print_vacancies(self, vacancies) -> None:
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
