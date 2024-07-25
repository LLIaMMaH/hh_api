# HeadHunter API

Получение информации о вакансиях при помощи api от сервиса HeadHunter.



## Зависимости

Библиотеки `requests`, `sqlite3`, `datetime` и `colorama`
```bash
  pip install requests sqlite3 datetime colorama 
```
* _А вдруг не установлено у кого-нибудь._

## Запуск

Запуск скрипт `hh_api.py` и отвечаем на вопросы

```bash
  python3 hh_api.py 
```


## Особенности

- Получение списка вакансий прямо в терминале


## Планы на будущее

- [ ] Сделать возможность кастомизации выводимых полей о вакансии
- [ ] Сохранять в базу полученные вакансии
- [ ] Возможность помечать вакансии на которые отправлялся отзыв (https://api.hh.ru/openapi/redoc#tag/Otklikipriglasheniya-rabotodatelya/operation/get-negotiations - https://api.hh.ru/negotiations)
- [ ] Возможность помечать вакансии на которые был получен ответ на отзыв (https://api.hh.ru/openapi/redoc#tag/Otklikipriglasheniya-rabotodatelya/operation/get-collection-negotiations-list - https://api.hh.ru/negotiations/response)
- [ ] Логирование в Sentry

