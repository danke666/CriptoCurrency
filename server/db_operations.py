import sqlite3
from datetime import datetime
import logging

DB_PATH = "db/database.sqlite"

# Функция для создания таблиц, если они не существуют
def create_tables():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Создание таблицы для истории цен
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS price_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cryptocurrency TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        price_usd REAL NOT NULL,
        price_eur REAL NOT NULL
    )
    ''')
    
    # Создание таблицы для конвертаций
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS conversions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cryptocurrency TEXT NOT NULL,
        amount REAL NOT NULL,
        currency TEXT NOT NULL,
        converted_amount REAL NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

# Функция для добавления записи в таблицу истории цен
def insert_price(cryptocurrency, price_usd, price_eur):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO price_history (cryptocurrency, price_usd, price_eur)
        VALUES (?, ?, ?)
        ''', (cryptocurrency, price_usd, price_eur))

        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Ошибка при вставке данных: {e}")
    finally:
        conn.close()

# Функция для получения истории цен
def get_price_history(cryptocurrency, limit=100):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
        SELECT timestamp, price_usd, price_eur
        FROM price_history
        WHERE cryptocurrency = ?
        ORDER BY timestamp DESC
        LIMIT ?
        ''', (cryptocurrency, limit))

        rows = cursor.fetchall()
        # Преобразование данных в словарь
        data = [{'timestamp': row[0], 'price_usd': row[1], 'price_eur': row[2]} for row in rows]
        return data
    except sqlite3.Error as e:
        logging.error(f"Ошибка при получении данных: {e}")
        return []
    finally:
        conn.close()

# Функция для добавления записи в таблицу конвертаций
def insert_conversion(cryptocurrency, amount, currency, converted_amount):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO conversions (cryptocurrency, amount, currency, converted_amount)
        VALUES (?, ?, ?, ?)
        ''', (cryptocurrency, amount, currency, converted_amount))

        conn.commit()
    except sqlite3.Error as e:
        logging.error(f"Ошибка при вставке данных: {e}")
    finally:
        conn.close()

# Создание таблиц при запуске модуля
create_tables()