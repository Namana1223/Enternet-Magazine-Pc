import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "db.sqlite3"

# ==============================
# Creare conexiune și inițializare tabele
# ==============================

def create_connection():
    return sqlite3.connect(DB_PATH)

def initialize_db():
    with create_connection() as conn:
        cursor = conn.cursor()
        # Tabel produse
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                image TEXT
            )
        """)
        # Tabel coș
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cart (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                FOREIGN KEY(product_id) REFERENCES products(id)
            )
        """)
        # Tabel comenzi
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                method TEXT NOT NULL,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

# ==============================
# Funcții produse
# ==============================

def get_all_products():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        return cursor.fetchall()

def get_product(product_id):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        return cursor.fetchone()

# ==============================
# Funcții coș
# ==============================

def add_to_cart(product_id):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cart (product_id) VALUES (?)", (product_id,))
        conn.commit()

def remove_from_cart(cart_id):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart WHERE id = ?", (cart_id,))
        conn.commit()

def get_cart_items():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT cart.id, products.name, products.price, products.image
            FROM cart
            JOIN products ON cart.product_id = products.id
        """)
        return cursor.fetchall()

def clear_cart():
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart")
        conn.commit()

# ==============================
# Funcții pentru checkout
# ==============================

def save_order(method):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO orders (method) VALUES (?)", (method,))
        conn.commit()
