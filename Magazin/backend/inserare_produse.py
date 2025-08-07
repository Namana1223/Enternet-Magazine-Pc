import sqlite3
from faker import Faker
import random
import os

DB_NAME = os.path.join(os.path.dirname(__file__), "store.db")
faker = Faker()

PRODUCT_IMAGE_URL = "https://i.pinimg.com/1200x/7b/30/6b/7b306bec5e7f33f4b16b214732459406.jpg"


def connect():
    return sqlite3.connect(DB_NAME)

def insert_products_only():
    conn = connect()
    cursor = conn.cursor()

    # ✅ Categoriile așteptate (trebuie să existe deja în DB)
    categories = ['Mouse', 'Tastatură', 'Memorie RAM']
    
    # Mapare nume categorie -> ID
    category_map = {}
    for name in categories:
        cursor.execute("SELECT id FROM product_categories WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            category_map[name] = result[0]
        else:
            print(f"⚠️ Categoria '{name}' nu există în DB. Omit.")

    # ✅ Inserare produse (3 per categorie existentă)
    products = []
    for cat_name, cat_id in category_map.items():
        for _ in range(3):
            name = f"{cat_name} {faker.word().capitalize()}"
            price = round(random.uniform(100, 800), 2)
            stock = random.randint(5, 50)
            image_url = PRODUCT_IMAGE_URL

            cursor.execute('''
                INSERT INTO products (name, price, stock, image_url, category_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, price, stock, image_url, cat_id))
            products.append((cursor.lastrowid, cat_id))
    conn.commit()

    # ✅ Adăugare atribute pentru noile produse
    cursor.execute("SELECT id, name, category_id FROM attributes")
    all_attributes = cursor.fetchall()

    for prod_id, cat_id in products:
        for attr_id, attr_name, attr_cat_id in all_attributes:
            if attr_cat_id == cat_id:
                value = (
                    str(random.randint(1600, 32000)) if "DPI" in attr_name or "Capacitate" in attr_name
                    else faker.word().capitalize()
                )
                cursor.execute('''
                    INSERT INTO product_attributes (product_id, attribute_id, value)
                    VALUES (?, ?, ?)
                ''', (prod_id, attr_id, value))
    conn.commit()
    conn.close()
    print("✅ Produse și atributele acestora au fost adăugate cu succes.")

if __name__ == "__main__":
    insert_products_only()
    
