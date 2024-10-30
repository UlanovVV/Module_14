import sqlite3


def initiate_db():
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    );
    ''')
    cursor.execute('DELETE FROM Products')

    for i in range(1, 5):
        cursor.execute('INSERT INTO Products (title, description, price) VALUES (?, ?, ?)',
                       (f'Продукт {i}', f'Описание {i}', f'{i*100}',))

    connection.commit()
    connection.close()

    connection = sqlite3.connect('Users.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
        )
    ''')

    connection.commit()
    connection.close()


def add_user(username, email, age, balance):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute('SELECT id, username, email, age, balance FROM Users')
    if not is_included(username):
        cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                       (username, email, age, balance))

    connection.commit()
    connection.close()


def is_included(username):
    connection = sqlite3.connect('Users.db')
    cursor = connection.cursor()
    check_name = cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    try:
        if check_name.fetchone()[1] == username:
            return True
    except TypeError:
        return False
    finally:
        connection.close()


def get_all_products():
    connection = sqlite3.connect('Products.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    db = cursor.fetchall()
    connection.commit()
    connection.close()
    return list(db)

