# HeadHunter API

Получение информации о вакансиях при помощи api от сервиса HeadHunter.



## Зависимости

Библиотеки `requests`, `sqlite3`, `datetime`, `colorama` [pypi](https://pypi.org/project/colorama/) [git](https://github.com/tartley/colorama) и `environs` [pypi](https://pypi.org/project/environs/) [git]((https://github.com/sloria/environs))
```bash
  pip install requests sqlite3 datetime colorama environs 
```
* _А вдруг не установлено у кого-нибудь._



## Получение client_id и client_secret для приложения
Теперь для работы приложения его необходимо зарегистрировать на сайте https://dev.hh.ru/admin.  
Переименовать файл .env.example в файл .env  и записать полученные данные. 



## Запуск

Запускаем скрипт и отвечаем на вопросы

```bash
  python3 main.py 
```


## Особенности

- Получение списка вакансий прямо в терминале
 






## Планы на будущее

- [ ] Сделать возможность кастомизации выводимых полей о вакансии
- [ ] Возможность помечать вакансии на которые отправлялся отзыв (https://api.hh.ru/openapi/redoc#tag/Otklikipriglasheniya-rabotodatelya/operation/get-negotiations - https://api.hh.ru/negotiations)
- [ ] Возможность помечать вакансии на которые был получен ответ на отзыв (https://api.hh.ru/openapi/redoc#tag/Otklikipriglasheniya-rabotodatelya/operation/get-collection-negotiations-list - https://api.hh.ru/negotiations/response)
- [ ] Логирование в Sentry
- [ ] [Просмотр конкретной вакансии](https://api.hh.ru/openapi/redoc#tag/Upravlenie-vakansiyami/operation/get-vacancy) (https://api.hh.ru/vacancies/{vacancy_id})

## Что сделано
- [X] Сохранять в базу полученные вакансии  
- [X] Получение токена для работы с сервисом и сохранением его для дальнейшей работы  


# Описание API
[HeadHunter API](https://github.com/hhru/api)