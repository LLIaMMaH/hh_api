import requests
from colorama import init, Fore, Style

class HeadHunterAPI:
    def __init__(self):
        self.base_url = "https://api.hh.ru"
    
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
    
    def print_vacancies(self, vacancies):
        """Вывод информации о вакансиях."""
        for item in vacancies['items']:
            print(f"{Fore.GREEN}Вакансия с id:{Style.RESET_ALL}: {Fore.YELLOW}{item['id']}")
            print(f"{Fore.GREEN}Название{Style.RESET_ALL}: {item['name']}")
            print(f"{Fore.GREEN}Компания{Style.RESET_ALL}: {item['employer']['name']}")
            print(f"{Fore.GREEN}Город{Style.RESET_ALL}: {item['area']['name']}")
            print(f"{Fore.GREEN}Опубликовано{Style.RESET_ALL}: {item['published_at']}")
            if item['salary'] is not None:
                salary_from = 0
                if item['salary']['from'] and str(item['salary']['from']).isnumeric():
                    salary_from = item['salary']['from']
                salary_to = 0
                if item['salary']['to'] and str(item['salary']['to']).isnumeric():
                    salary_to = item['salary']['to']
                if salary_from + salary_to > 0:
                    salary_to_string = ''
                    if salary_from > 0:
                        salary_to_string = 'От ' + str(salary_from)
                    if salary_to > 0:
                        if salary_to_string != '':
                            salary_to_string += ' '
                        salary_to_string += 'До ' + str(salary_to)
                    if item['salary']['currency'] != '':
                        salary_to_string += ' ' + str(item['salary']['currency'])
                    if salary_to_string != '':
                        print(f"{Fore.GREEN}Заработная плата{Style.RESET_ALL}: {salary_to_string}")
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

