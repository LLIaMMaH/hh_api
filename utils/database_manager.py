# -*- coding: utf-8 -*-

import datetime
import sqlite3


class DatabaseManager:
    def __init__(self, db_name='vacancies.db'):
        self.db_connection = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self) -> None:
        """Создание таблицы для хранения данных о вакансиях и токенов."""
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
                gross INTEGER,
                alternate_url TEXT,
                update_at TEXT
            )
            """)
            self.db_connection.execute("""
            CREATE TABLE IF NOT EXISTS tokens (
                token TEXT PRIMARY KEY,
                expires_in INTEGER,
                created_at TEXT
            )
            """)

    def save_vacancy(self, vacancy) -> None:
        """Сохраняем или обновляем информацию о вакансии в базе данных."""
        with self.db_connection:
            salary_from = vacancy['salary']['from'] if vacancy['salary'] else 0
            salary_to = vacancy['salary']['to'] if vacancy['salary'] else 0
            currency = vacancy['salary']['currency'] if vacancy['salary'] else None
            gross = vacancy['salary']['gross'] if vacancy['salary'] else False

            self.db_connection.execute("""
                INSERT OR REPLACE INTO vacancies (
                    id, name, employer, area, published_at, 
                    salary_from, salary_to, currency, gross, alternate_url, update_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                vacancy['id'],
                vacancy['name'],
                vacancy['employer']['name'],
                vacancy['area']['name'],
                vacancy['published_at'],
                salary_from,
                salary_to,
                currency,
                gross,
                vacancy['alternate_url'],
                datetime.datetime.now().isoformat(),
            ))

    def save_token(self, token, expires_in) -> None:
        """Сохраняем токен в базу данных."""
        with self.db_connection:
            self.db_connection.execute("""
                INSERT OR REPLACE INTO tokens (token, expires_in, created_at)
                VALUES (?, ?, ?)
            """, (
                token,
                expires_in,
                datetime.datetime.now().isoformat(),
            ))

    def get_token(self) -> tuple:
        """Получаем последний сохраненный токен, если он не истек."""
        with self.db_connection:
            cur = self.db_connection.cursor()
            cur.execute("""
                SELECT token, expires_in, created_at FROM tokens ORDER BY created_at DESC LIMIT 1
            """)
            row = cur.fetchone()
            if row:
                token, expires_in, created_at = row

                if not expires_in:
                    return None, None, None

                created_at = datetime.datetime.fromisoformat(created_at)
                expiration_time = created_at + datetime.timedelta(seconds=expires_in)

                if datetime.datetime.now() < expiration_time:
                    return token, expires_in, created_at

            return None, None, None

    def process_vacancies(self, vacancies) -> None:
        """Обрабатываем и сохраняем список вакансий."""
        for item in vacancies['items']:
            self.save_vacancy(item)

    def __del__(self):
        self.db_connection.close()
