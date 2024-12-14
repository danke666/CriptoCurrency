import sqlite3

# Путь к базе данных
DB_PATH = "db/database.sqlite"

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

    conn.commit()
    conn.close()
    print("Таблицы успешно созданы.")

if __name__ == "__main__":
    create_tables()
