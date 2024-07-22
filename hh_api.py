import requests

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
            print(f"Название: {item['name']}")
            print(f"Компания: {item['employer']['name']}")
            print(f"Город: {item['area']['name']}")
            print(f"Опубликовано: {item['published_at']}")
            print(f"Ссылка: {item['alternate_url']}")
            print("-" * 40)

if __name__ == "__main__":
    hh_api = HeadHunterAPI()
    search_text = input("Введите ключевые слова для поиска вакансий: ")
    area_number = int(input("Регион (1 - Москва, 2 - Санкт-Петербург): "))
    vacancies = hh_api.search_vacancies(search_text, area_number)
    hh_api.print_vacancies(vacancies)

