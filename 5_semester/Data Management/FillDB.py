import sqlite3
from datetime import datetime

# Создание и подключение базы данных
conn = sqlite3.connect("DreamHackers.db")
cursor = conn.cursor()

# Заполнение таблицы Genres
genres = [
    'Action', 'Adventure', 'RPG', 'Simulation', 'Strategy', 'Sports', 'Puzzle',
    'Horror', 'Fighting', 'Racing', 'Music', 'Party', 'Shooter', 'Survival', 'Stealth'
]

# Заполнение таблицы Games
games = [
    ("Cyberpunk 2077", 1, 59.99, "2020-12-10"),  # Action
    ("The Witcher 3: Wild Hunt", 3, 39.99, "2015-05-18"),  # RPG
    ("Minecraft", 4, 26.95, "2011-11-18"),  # Simulation
    ("Stardew Valley", 4, 14.99, "2016-02-26"),  # Simulation
    ("Hollow Knight", 3, 14.99, "2017-02-24"),  # RPG
    ("FIFA 23", 6, 59.99, "2022-09-30"),  # Sports
    ("Overwatch 2", 1, 0.00, "2022-10-04"),  # Action
    ("Civilization VI", 5, 59.99, "2016-10-21"),  # Strategy
    ("Portal 2", 7, 9.99, "2011-04-18"),  # Puzzle
    ("Red Dead Redemption 2", 2, 59.99, "2018-10-26"),  # Adventure
    ("Doom Eternal", 1, 59.99, "2020-03-20"),  # Action
    ("The Sims 4", 4, 39.99, "2014-09-02"),  # Simulation
    ("Assassin's Creed Valhalla", 2, 59.99, "2020-11-10"),  # Adventure
    ("Celeste", 7, 19.99, "2018-01-25"),  # Puzzle
    ("Dark Souls III", 3, 59.99, "2016-03-24"),  # RPG
    ("Sekiro: Shadows Die Twice", 3, 59.99, "2019-03-22"),  # RPG
    ("Animal Crossing: New Horizons", 4, 59.99, "2020-03-20"),  # Simulation
    ("Factorio", 5, 30.00, "2020-08-14"),  # Strategy
    ("League of Legends", 1, 0.00, "2009-10-27"),  # Action
    ("Apex Legends", 1, 0.00, "2019-02-04"),  # Action
    ("Call of Duty: Modern Warfare II", 1, 69.99, "2022-10-28"),  # Shooter
    ("The Legend of Zelda: Tears of the Kingdom", 2, 59.99, "2023-05-12"),  # Adventure
    ("Elden Ring", 3, 59.99, "2022-02-25"),  # RPG
    ("Gran Turismo 7", 6, 59.99, "2022-03-04"),  # Sports
    ("GTA V", 1, 29.99, "2013-09-17"),  # Action
    ("Resident Evil Village", 8, 39.99, "2021-05-07"),  # Horror
    ("Super Smash Bros. Ultimate", 8, 59.99, "2018-12-07"),  # Fighting
    ("Battlefield 2042", 1, 59.99, "2021-11-19"),  # Shooter
    ("FIFA 22", 6, 59.99, "2021-10-01"),  # Sports
    ("Fortnite", 1, 0.00, "2017-07-25"),  # Action
    ("Gran Turismo 5", 10, 39.99, "2010-11-24"),  # Racing
    ("Beat Saber", 11, 29.99, "2018-05-01"),  # Music
    ("Mario Kart 8 Deluxe", 10, 59.99, "2017-04-28"),  # Racing
    ("Just Dance 2023", 11, 39.99, "2023-11-22"),  # Music
    ("Worms Battlegrounds", 12, 19.99, "2014-06-03"),  # Party
    ("Overcooked! 2", 12, 24.99, "2018-08-07"),  # Party
    ("Resident Evil 7: Biohazard", 8, 29.99, "2017-01-24"),  # Horror
    ("Street Fighter V", 9, 39.99, "2016-02-16"),  # Fighting
    ("Hotline Miami", 13, 9.99, "2012-10-23"),  # Stealth
    ("Subnautica", 13, 29.99, "2018-01-23"),  # Survival
    ("Dead by Daylight", 8, 39.99, "2016-06-14"),  # Horror
    ("Hitman 3", 13, 59.99, "2021-01-20"),  # Stealth
    ("The Forest", 13, 19.99, "2018-04-30")  # Survival
]

# Заполнение таблицы Users
users = [
    ("Alice", "alice@example.com", "2023-01-10"),
    ("Bob", "bob@example.com", "2023-02-15"),
    ("Charlie", "charlie@example.com", "2023-03-20"),
    ("David", "david@example.com", "2023-04-25"),
    ("Eve", "eve@example.com", "2023-05-30"),
    ("Frank", "frank@example.com", "2023-06-05"),
    ("Grace", "grace@example.com", "2023-06-10"),
    ("Hannah", "hannah@example.com", "2023-06-15"),
    ("Ivan", "ivan@example.com", "2023-06-20"),
    ("Jack", "jack@example.com", "2023-06-25"),
    ("Kathy", "kathy@example.com", "2023-07-01"),
    ("Liam", "liam@example.com", "2023-07-05"),
    ("Mia", "mia@example.com", "2023-07-10"),
    ("Noah", "noah@example.com", "2023-07-15"),
    ("Olivia", "olivia@example.com", "2023-07-20"),
    ("Paul", "paul@example.com", "2023-07-25")
]

# Заполнение таблицы Wishlist
wishlist = [
    (1, 1, "2023-01-11"),  # Cyberpunk 2077
    (1, 2, "2023-01-12"),  # The Witcher 3: Wild Hunt
    (2, 3, "2023-02-16"),  # Minecraft
    (3, 4, "2023-03-21"),  # Stardew Valley
    (4, 5, "2023-04-26"),  # Hollow Knight
    (5, 6, "2023-05-10"),  # FIFA 23
    (1, 7, "2023-01-25"),  # Overwatch 2
    (2, 8, "2023-02-28"),  # Civilization VI
    (3, 9, "2023-03-10"),  # Portal 2
    (4, 10, "2023-04-15"),  # Red Dead Redemption 2
    (1, 11, "2023-06-01"),  # Doom Eternal
    (2, 12, "2023-06-05"),  # The Sims 4
    (3, 13, "2023-06-10"),  # Assassin's Creed Valhalla
    (4, 14, "2023-06-15"),  # Celeste
    (5, 15, "2023-06-20"),  # Dark Souls III
    (6, 16, "2023-07-01"),  # Sekiro: Shadows Die Twice
    (7, 17, "2023-07-05"),  # Animal Crossing: New Horizons
    (8, 18, "2023-07-10"),  # Factorio
    (9, 19, "2023-07-15"),  # League of Legends
    (10, 20, "2023-07-20"),  # Apex Legends
    (11, 21, "2023-07-25"),  # Call of Duty: Modern Warfare II
    (12, 22, "2023-08-01"),  # The Legend of Zelda: Tears of the Kingdom
    (13, 23, "2023-08-05"),  # Elden Ring
    (14, 24, "2023-08-10"),  # Gran Turismo 7
    (15, 25, "2023-08-15"),  # GTA V
    (16, 26, "2023-08-20"),  # Resident Evil Village
    (17, 27, "2023-08-25"),  # Super Smash Bros. Ultimate
    (18, 28, "2023-09-01"),  # Battlefield 2042
    (19, 29, "2023-09-05"),  # FIFA 22
    (20, 30, "2023-09-10"),  # Fortnite
    (21, 31, "2023-09-15"),  # Gran Turismo 5
    (22, 32, "2023-09-20"),  # Beat Saber
    (23, 33, "2023-09-25"),  # Mario Kart 8 Deluxe
    (24, 34, "2023-09-30"),  # Just Dance 2023
    (25, 35, "2023-10-05"),  # Worms Battlegrounds
    (26, 36, "2023-10-10"),  # Overcooked! 2
    (27, 37, "2023-10-15"),  # Resident Evil 7: Biohazard
    (28, 38, "2023-10-20"),  # Street Fighter V
    (29, 39, "2023-10-25"),  # Hotline Miami
    (30, 40, "2023-10-30"),  # Subnautica
    (31, 41, "2023-11-05")   # The Forest
]

# Заполнение таблицы Orders
orders = [ 
    (1, "2023-01-15"),  # Cyberpunk 2077
    (2, "2023-02-20"),  # The Witcher 3: Wild Hunt
    (3, "2023-03-25"),  # Minecraft
    (4, "2023-04-30"),  # Stardew Valley
    (5, "2023-05-05"),  # Hollow Knight
    (1, "2023-02-10"),  # FIFA 23
    (2, "2023-03-15"),   # Overwatch 2
    (3, "2023-04-05"),  # Civilization VI
    (4, "2023-05-01"),  # Portal 2
    (5, "2023-05-10"), # Red Dead Redemption 2
    (1, "2023-06-01"), # Doom Eternal
    (2, "2023-06-05"), # The Sims 4
    (3, "2023-06-10"), # Assassin's Creed Valhalla
    (4, "2023-06-15"), # Celeste
    (5, "2023-06-20"), # Dark Souls III
    (6, "2023-07-01"), # Sekiro: Shadows Die Twice
    (7, "2023-07-05"), # Animal Crossing: New Horizons
    (8, "2023-07-10"), # Factorio
    (9, "2023-07-15"), # League of Legends
    (10, "2023-07-20"),# Apex Legends
    (11, "2023-07-25"),# Call of Duty: Modern Warfare II
    (12, "2023-08-01"),# The Legend of Zelda: Tears of the Kingdom
    (13, "2023-08-05"),# Elden Ring
    (14, "2023-08-10"),# Gran Turismo 7
    (15, "2023-08-15"),# GTA V
    (16, "2023-08-20"),# Resident Evil Village
    (17, "2023-08-25"),# Super Smash Bros. Ultimate
    (18, "2023-09-01"),# Battlefield 2042
    (19, "2023-09-05"),# FIFA 22
    (20, "2023-09-10"),  # Fortnite
    (21, "2023-09-15"),# Gran Turismo 5
    (22, "2023-09-20"),# Beat Saber
    (23, "2023-09-25"),# Mario Kart 8 Deluxe
    (24, "2023-09-30"),# Just Dance 2023
    (25, "2023-10-05"),# Worms Battlegrounds
    (26, "2023-10-10"),# Overcooked! 2
    (27, "2023-10-15"),# Resident Evil 7: Biohazard
    (28, "2023-10-20"),# Street Fighter V
    (29, "2023-10-25"), # Hotline Miami
    (30, "2023-10-30"),# Subnautica
    (31, "2023-11-05") # The Forest
]

# Заполнение таблицы OrderList
orderlist_data = [
    (1, 1, 1),
    (1, 2, 2),
    (2, 3, 1),
    (3, 4, 1),
    (3, 5, 3),
    (4, 6, 2),
    (4, 7, 1),
    (5, 8, 4),
    (6, 9, 1),
    (6, 10, 1),
    (7, 11, 2),
    (7, 12, 2),
    (8, 13, 1),
    (9, 14, 3),
    (10, 15, 1)
]

# Код для вставки данных в базу данных
cursor.executemany("INSERT INTO Genres (genre_name) VALUES (?);", [(genre,) for genre in genres])
cursor.executemany("INSERT INTO Games (title, genre_id, price, release_date) VALUES (?, ?, ?, ?);", games)
cursor.executemany("INSERT INTO Users (username, email, registration_date) VALUES (?, ?, ?);", users)
cursor.executemany("INSERT INTO Wishlist (user_id, game_id, added_date) VALUES (?, ?, ?);", wishlist)
cursor.executemany("INSERT INTO Orders (user_id, order_date) VALUES (?, ?);", orders)
cursor.executemany("INSERT INTO OrderList (order_id, game_id, quantity) VALUES (?, ?, ?);", orderlist_data)

# Сохраняем изменения в базе данных
conn.commit()

# Закрываем соединение
conn.close()