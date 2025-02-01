import sqlite3
from datetime import datetime

# Создание и подключение базы данных
conn = sqlite3.connect("DreamHackers.db")
cursor = conn.cursor()

# Создание таблиц
cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        registration_date TEXT NOT NULL
);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Genres (
        genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
        genre_name TEXT NOT NULL UNIQUE
);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Games (
        game_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        genre_id INTEGER NOT NULL,
        price REAL NOT NULL,
        release_date TEXT NOT NULL,
        FOREIGN KEY (genre_id) REFERENCES Genres(genre_id)
);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS Orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        order_date TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES Users(user_id)
);
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS OrderList (
        orderlist_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        game_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (order_id) REFERENCES Orders (order_id),
        FOREIGN KEY (game_id) REFERENCES Games (game_id)
    );
""")

# Фиксация изменений
conn.commit()

# Закрытие соединения
conn.close()