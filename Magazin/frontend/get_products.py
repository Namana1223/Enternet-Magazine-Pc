import sqlite3
import json
import os

def get_products():
    # Conectare la baza de date
    db_path = os.path.join(os.path.dirname(__file__), '..', 'backend', 'store.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Query pentru toate produsele cu categorie și atribute
    cursor.execute('''
        SELECT 
            p.id,
            p.name,
            p.price,
            p.stock,
            p.image_url,
            pc.name as category_name,
            GROUP_CONCAT(a.name || ': ' || pa.value) as attributes
        FROM products p
        LEFT JOIN product_categories pc ON p.category_id = pc.id
        LEFT JOIN product_attributes pa ON p.id = pa.product_id
        LEFT JOIN attributes a ON pa.attribute_id = a.id
        GROUP BY p.id
        ORDER BY p.name
    ''')
    
    products = []
    for row in cursor.fetchall():
        product_id, name, price, stock, image_url, category_name, attributes_str = row
        
        # Procesare atribute
        attributes = {}
        if attributes_str:
            for attr_pair in attributes_str.split(','):
                if ':' in attr_pair:
                    attr_name, attr_value = attr_pair.split(':', 1)
                    attributes[attr_name.strip()] = attr_value.strip()
        
        product = {
            'id': product_id,
            'name': name,
            'price': price,
            'stock': stock,
            'image_url': image_url,
            'category': category_name,
            'attributes': attributes
        }
        products.append(product)
    
    conn.close()
    return products

def save_products_to_json():
    products = get_products()
    with open('products.json', 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=4)
    print(f"✅ {len(products)} produse salvate în products.json")

if __name__ == "__main__":
    save_products_to_json()