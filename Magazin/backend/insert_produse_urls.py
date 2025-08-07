import sqlite3
from faker import Faker
import random
import os

DB_NAME = os.path.join(os.path.dirname(__file__), "store.db")
faker = Faker()

# ✅ Linkuri imagini pentru produse – UN LINK = UN PRODUS
PRODUCT_IMAGE_URLS = [
    "https://i.pinimg.com/1200x/7b/30/6b/7b306bec5e7f33f4b16b214732459406.jpg",
    "https://i.pinimg.com/1200x/8c/11/fd/8c11fd49b6dd72cb0eacc4ae4db4600b.jpg",
    "https://i.pinimg.com/1200x/cc/e2/e1/cce2e1d7d8c12e1aa09e1dcf42013c89.jpg",
    "https://i.pinimg.com/1200x/40/fb/2f/40fb2f367b92eb939eb92863cf3c4f78.jpg"
]

def connect():
    return sqlite3.connect(DB_NAME)

def insert_products_from_image_list():
    conn = connect()
    cursor = conn.cursor()

    categories = ['Mouse', 'Tastatură', 'Memorie RAM']

    # Obține ID-uri pentru categorii existente
    category_map = {}
    for name in categories:
        cursor.execute("SELECT id FROM product_categories WHERE name = ?", (name,))
        result = cursor.fetchone()
        if result:
            category_map[name] = result[0]
        else:
            print(f"⚠️ Categoria '{name}' nu există. Omit.")

    if not category_map:
        print("❌ Nu s-au găsit categorii existente. Ieșire.")
        return

    category_ids = list(category_map.values())
    products = []

    # Generează produse pe baza imaginilor
    for index, image_url in enumerate(PRODUCT_IMAGE_URLS):
        category_id = category_ids[index % len(category_ids)]
        category_name = [k for k, v in category_map.items() if v == category_id][0]

        name = f"{category_name} {faker.word().capitalize()}"
        price = round(random.uniform(100, 800), 2)
        stock = random.randint(5, 50)

        cursor.execute('''
            INSERT INTO products (name, price, stock, image_url, category_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, price, stock, image_url, category_id))

        products.append((cursor.lastrowid, category_id))
    conn.commit()

    # Adaugă atribute produselor
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
    print(f"✅ {len(products)} produse au fost adăugate cu imaginile specificate.")

if __name__ == "__main__":
    insert_products_from_image_list()