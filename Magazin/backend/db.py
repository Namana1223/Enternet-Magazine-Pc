import sqlite3
import os

#  Salvează baza de date în același director cu acest fișier
DB_NAME = os.path.join(os.path.dirname(__file__), "store.db")

def connect():
    return sqlite3.connect(DB_NAME)

def reset_database():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)

def create_tables():
    conn = sqlite3.connect('store.db')
    cursor = conn.cursor()
    
    #  Tabel categorii produse
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS product_categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        image_url TEXT
    )
    ''')
    
    #  Tabel atribute
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS attributes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES product_categories(id)
    )
    ''')
    
    #  Tabel atribute produse
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS product_attributes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_id INTEGER,
        attribute_id INTEGER,
        value TEXT,
        FOREIGN KEY (product_id) REFERENCES products(id),
        FOREIGN KEY (attribute_id) REFERENCES attributes(id)
    )
    ''')
    
    #  Tabel produse
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL,
        image_url TEXT,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES product_categories(id)
    )
    ''')
    
    #  Tabel utilizatori
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        first_name TEXT,
        last_name TEXT,
        phone TEXT,
        address TEXT,
        city TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    #  Tabel coș utilizatori
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_carts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        product_image TEXT,
        product_price TEXT NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    ''')
    
    #  Tabel comenzi
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        total_amount REAL NOT NULL,
        status TEXT DEFAULT 'pending',
        payment_method TEXT,
        shipping_address TEXT,
        city TEXT,
        phone TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')
    
    #  Tabel detalii comenzi
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        product_price TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
    )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
    print("Tabelele au fost create cu succes!")