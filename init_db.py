import sqlite3

# Създаване на връзка към база данни (ще я създадем ако не съществува)
conn = sqlite3.connect('cars.db')

# Създаваме курсор за изпълнение на SQL команди
c = conn.cursor()

# Създаване на таблица за колите
c.execute('''
CREATE TABLE IF NOT EXISTS Cars (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    make TEXT NOT NULL,
    model TEXT NOT NULL,
    year INTEGER NOT NULL,
    price REAL NOT NULL,
    status TEXT NOT NULL
)
''')

# Създаване на таблица за разходи по кола
c.execute('''
CREATE TABLE IF NOT EXISTS Car_Expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    car_id INTEGER NOT NULL,
    expense_date TEXT NOT NULL,
    amount REAL NOT NULL,
    description TEXT,
    FOREIGN KEY (car_id) REFERENCES Cars (id)
)
''')

# Записваме промените и затваряме връзката
conn.commit()
conn.close()

print("Database and tables initialized successfully!")
