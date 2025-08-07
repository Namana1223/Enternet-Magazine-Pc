from backend.db import connect

def add_product(name, price, stock):
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
    conn.commit()
    conn.close()

def get_all_products():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()
    conn.close()
    return products
